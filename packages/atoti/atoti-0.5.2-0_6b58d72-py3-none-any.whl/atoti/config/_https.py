from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .._path_utils import PathLike, to_absolute_path
from ._utils import Configuration


@dataclass(frozen=True)
class HttpsConfiguration(Configuration):

    certificate: str
    password: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_https_config(**data)


def create_https_config(*, certificate: PathLike, password: str) -> HttpsConfiguration:
    """Create a PKCS 12 keystore configuration.

    Note:
        PEM or DER certificates can be `converted to PKCS 12 with OpenSSL <https://stackoverflow.com/questions/56241667/convert-certificate-in-der-or-pem-to-pkcs12/56244685#56244685>`_.

    Args:
        certificate: The path to the certificate.
        password: The password to read the certificate.

    Example:
        >>> python_config = tt.config.create_config(
        ...     https=tt.config.create_https_config(
        ...         certificate="../cert.p12", password="changeit"
        ...     )
        ... )
        >>> yaml_config = '''
        ... https:
        ...   certificate: ../cert.p12
        ...   password: changeit
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)
    """
    return HttpsConfiguration(
        certificate=to_absolute_path(certificate),
        password=password,
    )
