from typing import Any, Mapping

from ._auth import Auth
from ._auth_basic import BASIC_AUTH_TYPE, BasicAuthentication
from ._kerberos import KERBEROS_AUTH_TYPE, KerberosAuthentication
from ._ldap import LDAP_AUTH_TYPE, LdapAuthentication
from ._oidc import OIDC_AUTH_TYPE, OidcAuthentication
from .parsing import ConfigParsingError

_AUTH_TYPES = [BASIC_AUTH_TYPE, OIDC_AUTH_TYPE, LDAP_AUTH_TYPE]


def parse_auth(data: Mapping[str, Any]) -> Auth:
    """Parse the authentication."""
    if len(data) > 1:
        raise ConfigParsingError("Only one authentication type can be used.")
    if OIDC_AUTH_TYPE in data:
        return OidcAuthentication._from_dict(data[OIDC_AUTH_TYPE])
    if BASIC_AUTH_TYPE in data:
        return BasicAuthentication._from_dict(data[BASIC_AUTH_TYPE])
    if LDAP_AUTH_TYPE in data:
        return LdapAuthentication._from_dict(data[LDAP_AUTH_TYPE])
    if KERBEROS_AUTH_TYPE in data:
        return KerberosAuthentication._from_dict(data[KERBEROS_AUTH_TYPE])
    raise ConfigParsingError(f"Supported authentication types are {_AUTH_TYPES}")
