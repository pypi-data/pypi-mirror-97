from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Collection, Mapping, Optional

from ._auth import Auth
from ._utils import Configuration

BASIC_AUTH_TYPE = "basic"
ROLE_USER = "ROLE_USER"


@dataclass(frozen=True)
class BasicUser(Configuration):
    """Basic user with roles."""

    name: str
    password: str
    roles: Collection[str] = field(default_factory=list)

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_basic_user(**data)


def create_basic_user(
    name: str, password: str, *, roles: Optional[Collection[str]] = None
) -> BasicUser:
    """Create a basic user with roles.

    Args:
        name: The username.
        password: The password of the user.
        roles: The roles given to the user.
            The role ``ROLE_USER``, which is required to access the application, will automatically be added to the passed roles.
    """
    roles = set(roles) if roles is not None else set()
    roles.add(ROLE_USER)
    # Convert back to list so the class is JSON serializable
    return BasicUser(name, password, list(roles))


@dataclass(frozen=True)
class BasicAuthentication(Auth):
    """Basic authentication."""

    _name: str
    users: Collection[BasicUser]
    realm: Optional[str] = None

    @property
    def _type(self):
        return BASIC_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]) -> BasicAuthentication:
        """Create the authentication from dictionary."""
        data_dict = dict(data)
        users_data = data_dict.pop("users")
        users = [BasicUser._from_dict(user) for user in users_data]
        return create_basic_authentication(users, **data_dict)


def create_basic_authentication(
    users: Collection[BasicUser], *, realm: Optional[str] = None
) -> BasicAuthentication:
    """Create a basic authentication config.

    Basic authentication is the easiest way to get started with security since it only requires defining the users, their password, and their roles.

    Args:
        users: The users that can authenticate against the session.
        realm: The realm describing the protected area.
            Different realms can be used to isolate sessions running on the same domain (regardless of the port).
            The realm will also be displayed by the browser when prompting for credentials.
            Defaults to ``f"{session_name} atoti session at {session_id}"``.

    Example:
        >>> python_config = tt.config.create_config(
        ...     authentication=tt.config.create_basic_authentication(
        ...         users=[
        ...             tt.config.create_basic_user(
        ...                 "admin", "passwd", roles=["ROLE_ADMIN"]
        ...             ),
        ...             tt.config.create_basic_user(
        ...                 "user1", "passwd", roles=["ROLE_FRANCE"]
        ...             ),
        ...             tt.config.create_basic_user(
        ...                 "user2", "passwd", roles=["ROLE_UK"]
        ...             ),
        ...         ],
        ...         realm="Example",
        ...     )
        ... )
        >>> yaml_config = '''
        ... authentication:
        ...   basic:
        ...     users:
        ...       - name: admin
        ...         password: passwd
        ...         roles:
        ...           - ROLE_ADMIN
        ...       - name: user1
        ...         password: passwd
        ...         roles:
        ...           - ROLE_FRANCE
        ...       - name: user2
        ...         password: passwd
        ...         roles:
        ...           - ROLE_UK
        ...     realm: Example
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return BasicAuthentication("basic", users, realm)
