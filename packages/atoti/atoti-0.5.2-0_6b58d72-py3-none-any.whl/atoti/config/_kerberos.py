from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Collection, Mapping, Optional, Union

from .._path_utils import to_absolute_path
from ._auth import Auth
from ._utils import Configuration

KERBEROS_AUTH_TYPE = "kerberos"
ROLE_USER = "ROLE_USER"


@dataclass(frozen=True)
class KerberosUser(Configuration):
    """Kerberos user with roles."""

    name: str
    roles: Collection[str] = field(default_factory=list)

    @classmethod
    def _create(cls, data: Mapping[str, Any]) -> KerberosUser:
        return create_kerberos_user(**data)


def create_kerberos_user(
    *, name: str, roles: Optional[Collection[str]] = None
) -> KerberosUser:
    """Create a kerberos user with roles.

    Args:
        name: The useranme.
        roles: The roles given to the user.
            The role ``ROLE_USER`` which is required to access the application, will automatically be added to the passed roles.
    """
    roles = set(roles) if roles is not None else set()
    roles.add(ROLE_USER)
    # Convert to list because set is not JSON serializable
    return KerberosUser(name, list(roles))


@dataclass(frozen=True)
class KerberosAuthentication(Auth):
    """Kerberos authentication."""

    _name: str
    keytab: Union[str, Path]
    service_principal: str
    krb5_config: Optional[Union[str, Path]]
    users: Collection[KerberosUser]

    @property
    def _type(self):
        return KERBEROS_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        data_dict = dict(data)
        users_data = data_dict.pop("users")
        users = [KerberosUser._from_dict(user) for user in users_data]
        return create_kerberos_authentication(users=users, **data_dict)


def create_kerberos_authentication(
    *,
    service_principal: str,
    keytab: Union[Path, str],
    users: Collection[KerberosUser],
    krb5_config: Optional[Union[str, Path]] = None,
) -> KerberosAuthentication:
    """Create a kerberos authentication config.

    Atoti+ can be connected to Kerberos authentication network as a service.

    Args:
        service_principal: The principal the atoti application should use.
        keytab: The path to the keytab file to use.
        users: The kerberos users.
        krb5_config: The path to the kerberos config file. Defaults to the default location for the file on .

    Example:
        >>> python_config = tt.config.create_config(
        ...     authentication=tt.config.create_kerberos_authentication(
        ...         service_principal="HTTP/localhost",
        ...         keytab="config/example.keytab",
        ...         krb5_config="config/example.krb5",
        ...         users=[
        ...             tt.config.create_kerberos_user(
        ...                 name="admin", roles=["ROLE_ADMIN"]
        ...             ),
        ...             tt.config.create_kerberos_user(
        ...                 name="user1", roles=["ROLE_FRANCE"]
        ...             ),
        ...             tt.config.create_kerberos_user(name="user2", roles=["ROLE_UK"]),
        ...         ],
        ...     )
        ... )
        >>> yaml_config = '''
        ... authentication:
        ...   kerberos:
        ...     service_principal: HTTP/localhost
        ...     keytab: config/example.keytab
        ...     krb5_config: config/example.krb5
        ...     users:
        ...       - name: admin
        ...         roles:
        ...           - ROLE_ADMIN
        ...       - name: user1
        ...         roles:
        ...           - ROLE_FRANCE
        ...       - name: user2
        ...         roles:
        ...           - ROLE_UK
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)
    """
    if isinstance(keytab, Path):
        keytab = to_absolute_path(keytab)
    if krb5_config is not None and isinstance(krb5_config, Path):
        krb5_config = to_absolute_path(krb5_config)
    return KerberosAuthentication(
        _name="kerberos",
        service_principal=service_principal,
        keytab=keytab,
        krb5_config=krb5_config,
        users=users,
    )
