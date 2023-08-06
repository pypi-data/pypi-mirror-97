from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .._plugins import MissingPluginError, is_plugin_active
from ._cloud_utils import _parse_client_side_encryption
from ._utils import Configuration

AZURE_KEY_PAIR_TYPE = "key_pair"


@dataclass(frozen=True)
class AzureConfiguration(Configuration):

    client_side_encryption: AzureKeyPair

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        data_dict = dict(data)

        return create_azure_config(
            **{
                "client_side_encryption": _parse_client_side_encryption(
                    data_dict.pop("client_side_encryption"),
                    {
                        AZURE_KEY_PAIR_TYPE: AzureKeyPair,
                    },
                    "Azure",
                )
                if "client_side_encryption" in data_dict
                else None
            },
            **data_dict,
        )


def create_azure_config(
    *,
    client_side_encryption: AzureKeyPair,
) -> AzureConfiguration:
    """Create an Azure configuration.

    Note:
        This function requires the :mod:`atoti-azure <atoti_azure>` plugin.

    Args:
        client_side_encryption: The client side encryption mechanism to use when loading data from Azure.
    """
    if not is_plugin_active("azure"):
        raise MissingPluginError("azure")
    return AzureConfiguration(client_side_encryption=client_side_encryption)


@dataclass(frozen=True)
class AzureKeyPair(Configuration):

    key_id: str
    private_key: str
    public_key: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_azure_key_pair(**data)


def create_azure_key_pair(
    *, key_id: str, public_key: str, private_key: str
) -> AzureKeyPair:
    """Create an Azure Key Pair for client side encryption.

    Args:
        key_id: The id of the key used to encrypt the blob.
        public_key: The public key.
        private_key: The private key.

    Example:
        >>> python_config = tt.config.create_config(
        ...     azure=tt.config.create_azure_config(
        ...         client_side_encryption=tt.config.create_azure_key_pair(
        ...             key_id="aaa", public_key="yyy", private_key="xxx"
        ...         ),
        ...     )
        ... )
        >>> yaml_config = '''
        ... azure:
        ...     client_side_encryption:
        ...         key_pair:
        ...             key_id: aaa
        ...             private_key: xxx
        ...             public_key: yyy
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    .. warning::

        Each encrypted blob must have the metadata attribute ``unencrypted_content_length`` with the unencrypted file size.
        If this is not set, an :guilabel:`Issue while downloading` error will occur.
    """
    return AzureKeyPair(key_id=key_id, public_key=public_key, private_key=private_key)
