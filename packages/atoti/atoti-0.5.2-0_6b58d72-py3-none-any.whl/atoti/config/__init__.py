from __future__ import annotations

import os.path
from pathlib import Path
from typing import Optional, Union

import yaml

from ._auth_basic import create_basic_authentication, create_basic_user
from ._aws import create_aws_config, create_aws_key_pair, create_aws_kms_config
from ._azure import create_azure_config, create_azure_key_pair
from ._branding import create_branding
from ._https import create_https_config
from ._jwt import create_jwt_key_pair
from ._kerberos import create_kerberos_authentication, create_kerberos_user
from ._ldap import create_ldap_authentication
from ._oidc import create_oidc_authentication
from ._role import create_role
from ._session_configuration import SessionConfiguration, create_config, merge_config
from ._utils import _get_default_config_path
from ._yaml_utils import EnvVarLoader

DEFAULT_URL_PATTERN = "http://localhost:{port}"


def _parse_yaml_file_to_config(path: Path) -> SessionConfiguration:
    """Parse a YAML config file."""
    config_data = yaml.load(open(path), Loader=EnvVarLoader)  # nosec
    return SessionConfiguration._from_dict(config_data)


def _get_merged_config(
    provided_config: Optional[Union[SessionConfiguration, Path, str]]
) -> SessionConfiguration:
    """Get the config merged from the provided one and the default one.

    Args:
        provided_config: the config provided to the user.
            Either the object or a path.
        merge: Whether to merge the provided config with the default one.

    Returns:
        The configuration, merged with the default if necessary.

    """
    if isinstance(provided_config, str):
        provided_config = Path(provided_config)
    if isinstance(provided_config, Path):
        provided_config = _parse_yaml_file_to_config(provided_config)
    if provided_config is not None and provided_config.inherit_global_config is False:
        return provided_config
    default_path = _get_default_config_path()
    if default_path is None or not os.path.isfile(default_path):
        merged = provided_config
    else:
        merged = merge_config(_parse_yaml_file_to_config(default_path), provided_config)
    return merged if merged is not None else create_config()


__all__ = [
    "create_aws_config",
    "create_aws_key_pair",
    "create_aws_kms_config",
    "create_azure_config",
    "create_azure_key_pair",
    "create_basic_authentication",
    "create_basic_user",
    "create_branding",
    "create_config",
    "create_https_config",
    "create_jwt_key_pair",
    "create_kerberos_authentication",
    "create_kerberos_user",
    "create_ldap_authentication",
    "create_oidc_authentication",
    "create_role",
]
