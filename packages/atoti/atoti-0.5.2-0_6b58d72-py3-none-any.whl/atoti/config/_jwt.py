from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Mapping

from ._utils import Configuration


def is_base64(value: str) -> bool:
    """Check if a string is base64 encoded."""
    try:
        return base64.b64encode(base64.b64decode(value)).decode("ascii") == value
    except Exception:  # pylint: disable=broad-except
        return False


def get_base64_encoded(value: str) -> str:
    """Get the base64 encoded string."""
    if is_base64(value):
        return value

    return base64.b64encode(value.encode("ascii")).decode("ascii")


@dataclass(frozen=True)
class JwtKeyPair(Configuration):

    public_key: str
    private_key: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_jwt_key_pair(**data)


def create_jwt_key_pair(*, public_key: str, private_key: str) -> JwtKeyPair:
    """Return a key pair to sign JSON Web Tokens.

    Atoti+ uses JSON Web Tokens to authenticate communications between its various components (e.g. between the app and the session), but also to authenticate communications with remote metadata DBs.
    By default, a random key pair of 2048 bytes will be generated at session creation time and used to sign JWTs, but custom RSA key pairs can be set, mainly for SSO purposes.

    Only RSA keys using the PKCS 8 standard are supported.
    A key pair can be generated using a library like ``pycryptodome`` for example.

    Example:
        >>> python_config = tt.config.create_config(
        ...     jwt_key_pair=tt.config.create_jwt_key_pair(
        ...         public_key="public", private_key="private"
        ...     )
        ... )
        >>> yaml_config = '''
        ... jwt_key_pair:
        ...   public_key: public
        ...   private_key: private
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    public_key = get_base64_encoded(public_key)
    private_key = get_base64_encoded(private_key)
    return JwtKeyPair(public_key=public_key, private_key=private_key)
