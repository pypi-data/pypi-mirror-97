from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Union

from ._cloud_utils import _parse_client_side_encryption
from ._utils import Configuration

KMS_TYPE = "kms"
AWS_KEY_PAIR_TYPE = "key_pair"


@dataclass(frozen=True)
class AwsConfiguration(Configuration):

    region: str
    client_side_encryption: Optional[Union[AwsKeyPair, AwsKmsConfiguration]]

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        data_dict = dict(data)

        return create_aws_config(
            **{
                "client_side_encryption": _parse_client_side_encryption(
                    data_dict.pop("client_side_encryption"),
                    {KMS_TYPE: AwsKmsConfiguration, AWS_KEY_PAIR_TYPE: AwsKeyPair},
                    "AWS",
                )
                if "client_side_encryption" in data_dict
                else None
            },
            **data_dict,
        )


def create_aws_config(
    *,
    region: str,
    client_side_encryption: Optional[Union[AwsKeyPair, AwsKmsConfiguration]] = None,
) -> AwsConfiguration:
    """Create an AWS configuration.

    Note:
        This function requires the :mod:`atoti-aws <atoti_aws>` plugin.

    Args:
        client_side_encryption: The `client side encryption <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`_ mechanism to use when loading data from AWS.
        region: The AWS region to interact with.
            Required for client side encryption.

            AWS KMS CMK must have been created in the same AWS region as the destination bucket (cf. `AWS documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-config-for-kms-objects.html>`_).

    Example:
        >>> python_config = tt.config.create_config(
        ...     aws=tt.config.create_aws_config(
        ...         region="us-east-1",
        ...     )
        ... )
        >>> yaml_config = '''
        ... aws:
        ...   region: us-east-1
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return AwsConfiguration(
        region=region, client_side_encryption=client_side_encryption
    )


@dataclass(frozen=True)
class AwsKeyPair(Configuration):

    private_key: str
    public_key: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_aws_key_pair(**data)


def create_aws_key_pair(*, public_key: str, private_key: str) -> AwsKeyPair:
    """Create an AWS Key Pair for client side encryption.

    Args:
        public_key: The public key.
        private_key: The private key.

    Example:
        >>> python_config = tt.config.create_config(
        ...     aws=tt.config.create_aws_config(
        ...         client_side_encryption=tt.config.create_aws_key_pair(
        ...             public_key="public", private_key="private"
        ...         ),
        ...         region="us-east-1",
        ...     )
        ... )
        >>> yaml_config = '''
        ... aws:
        ...   client_side_encryption:
        ...     key_pair:
        ...       public_key: public
        ...       private_key: private
        ...   region: us-east-1
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return AwsKeyPair(public_key=public_key, private_key=private_key)


@dataclass(frozen=True)
class AwsKmsConfiguration(Configuration):

    key_id: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_aws_kms_config(**data)


def create_aws_kms_config(*, key_id: str) -> AwsKmsConfiguration:
    """Create an AWS KMS configuration for client side encryption.

    Args:
        key_id: The key id to identify the key in the KMS.

    Example:
        >>> python_config = tt.config.create_config(
        ...     aws=tt.config.create_aws_config(
        ...         client_side_encryption=tt.config.create_aws_kms_config(
        ...             key_id="abcd1234-12ab"
        ...         ),
        ...         region="us-east-1",
        ...     )
        ... )
        >>> yaml_config = '''
        ... aws:
        ...   client_side_encryption:
        ...     kms:
        ...       key_id: abcd1234-12ab
        ...   region: us-east-1
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return AwsKmsConfiguration(key_id=key_id)
