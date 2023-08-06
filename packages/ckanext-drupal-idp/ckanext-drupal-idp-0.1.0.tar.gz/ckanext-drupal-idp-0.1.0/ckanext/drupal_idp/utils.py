from __future__ import annotations

import base64
import hashlib
import logging
import six
import secrets
from typing import Any, Dict, List, Optional, TypedDict


import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.lib.munge as munge

CONFIG_DB_URL = "ckanext.drupal_idp.db_url"
CONFIG_SYNCHRONIZATION_ENABLED = "ckanext.drupal_idp.synchronization.enabled"
CONFIG_STATIC_HOST = "ckanext.drupal_idp.host"
CONFIG_INHERIT_ADMIN_ROLE = "ckanext.drupal_idp.admin_role.inherit"
CONFIG_ADMIN_ROLE_NAME = "ckanext.drupal_idp.admin_role.name"
CONFIG_DRUPAL_VERSION = "ckanext.drupal_idp.drupal.version"

DEFAULT_ADMIN_ROLE = "administrator"
DEFAULT_DRUPAL_VERSION = "9"

log = logging.getLogger(__name__)

DrupalId = int
UserDict = Dict[str, Any]


class DetailsData(TypedDict):
    name: str
    email: str
    id: DrupalId
    roles: List[str]


class Details:
    _props = ("name", "email", "id", "roles")
    name: str
    email: str
    id: DrupalId
    roles: List[str] = []

    def __init__(self, data: DetailsData):
        for k, v in data.items():
            if k not in self._props:
                continue
            setattr(self, k, v)

    def __iter__(self):
        for prop in self._props:
            yield prop, getattr(self, prop)

    def is_sysadmin(self):
        return (
            tk.asbool(tk.config.get(CONFIG_INHERIT_ADMIN_ROLE))
            and tk.config.get(CONFIG_ADMIN_ROLE_NAME, DEFAULT_ADMIN_ROLE)
            in self.roles
        )

    def make_userdict(self):
        return {
            "email": self.email,
            "name": munge.munge_name(self.name),
            "sysadmin": self.is_sysadmin(),
            "plugin_extras": {"drupal_idp": dict(self)},
        }


def is_synchronization_enabled() -> bool:
    return tk.asbool(tk.config.get(CONFIG_SYNCHRONIZATION_ENABLED))


def _make_password():
    return secrets.token_urlsafe(60)


def _get_host() -> str:
    host = tk.config.get(CONFIG_STATIC_HOST)
    if not host:
        host = tk.request.environ["HTTP_HOST"].split(":")[0]
    return host


def session_cookie_name() -> str:
    """Compute name of the cookie that stores Drupal's SessionID.

    For D9 it's PREFIX + HASH, where:
      PREFIX: if isHTTPS then SSESS else SESS
      HASH: first 32 characters of sha256 hash of the site's hostname
            (does not include port)

    """
    server_name = _get_host()
    hash = hashlib.sha256(six.ensure_binary(server_name)).hexdigest()[:32]
    name = f"SESS{hash}"
    if tk.config["ckan.site_url"].startswith("https"):
        name = "S" + name
    return name


def decode_sid(cookie_sid: str) -> str:
    """Decode Drupal's session cookie and turn it into SessionID.

    This method was written around Drupal v9.1.4 release. It's
    logic is unlikely to change for D9, but it may change in the
    future major releases, so keep an eye on it and check it first
    if you are sure that session cookie is there, but CKAN can't
    obtain user from Drupal's database.

    Algorythm:
    - get cookie value
    - sha256 it
    - base64 it
    - replace pluses and slashes
    - strip out `=`-paddings

    """
    sha_hash = hashlib.sha256(six.ensure_binary(cookie_sid)).digest()
    base64_hash = base64.encodebytes(sha_hash)
    trans_rules = str.maketrans(
        {
            "+": "-",
            "/": "_",
            "=": "",
        }
    )
    sid = six.ensure_str(base64_hash.strip()).translate(trans_rules)
    return sid


def get_user_details(sid: str) -> Optional[Details]:
    """Fetch user data from Drupal's database."""
    import ckanext.drupal_idp.drupal as drupal

    adapter = drupal.get_adapter(
        tk.config.get(CONFIG_DRUPAL_VERSION, DEFAULT_DRUPAL_VERSION)
    )
    user = adapter.get_user_by_sid(sid)
    # check if session has username,
    # otherwise is unauthenticated user session
    if not user:
        return
    details_data = DetailsData(**user)
    roles = adapter.get_user_roles(user.id)
    details_data["roles"] = roles
    return Details(details_data)


def _get_by_id(id: DrupalId) -> Optional[UserDict]:
    user = (
        model.Session.query(model.User.id)
        .filter(model.User.plugin_extras["drupal_idp"]["id"].astext == str(id))
        .one_or_none()
    )
    if user is None:
        return
    return tk.get_action("user_show")({"ignore_auth": True}, {"id": user.id})


def _get_by_email(email: str) -> Optional[UserDict]:
    user = (
        model.Session.query(model.User.id)
        .filter(model.User.email == email)
        .one_or_none()
    )
    if user is None:
        return
    return tk.get_action("user_show")({"ignore_auth": True}, {"id": user.id})


def _create_from_details(details: Details) -> UserDict:
    """Create a user with random password using Drupal's data.

    Raises:
    ValidationError if email or username is not unique
    """
    user = details.make_userdict()
    user["password"] = _make_password()

    admin = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    user = tk.get_action("user_create")({"user": admin["name"]}, user)
    return user


def _attach_details(id: str, details: Details) -> UserDict:
    """Update name, email and plugin_extras

    Raises:
    ValidationError if email or username is not unique
    """
    admin = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    user = tk.get_action("user_show")({"user": admin["name"]}, {"id": id})
    user.update(details.make_userdict())
    # user_patch is not available in v2.9
    user = tk.get_action("user_update")({"user": admin["name"]}, user)
    return user


def get_or_create_from_details(details: Details) -> UserDict:
    """Get existing user or create new one.

    Raises:
    ValidationError if email or username is not unique
    """
    user = _get_by_id(details.id)
    if user:
        return user

    user = _get_by_email(details.email)
    if user:
        return _attach_details(user["id"], details)
    return _create_from_details(details)


def synchronize(user: UserDict, details: Details) -> UserDict:
    userobj = model.User.get(user["id"])
    if userobj.name != details.name:
        log.info(f"Synchronizing user {userobj.name} -> {details.name}")
        if model.User.get(details.name) is not None:
            raise tk.ValidationError(
                {"name": "This username is already taken"}
            )
        userobj.name = details.name
        model.Session.commit()
    if (
        userobj.email != details.email
        or userobj.sysadmin != details.is_sysadmin()
    ):
        log.info(f"Synchronizing user {details.name}")
        user = _attach_details(user["id"], details)
    return user
