from __future__ import annotations

from typing import Any, Mapping

from .parsing import ConfigParsingError


def _parse_client_side_encryption(
    data: Mapping[str, Any],
    supported_encryptions: Mapping[
        str, Any
    ],  # Any since Configuration is throwing with TypeVar "_VT_co" is covariant
    cloud_provider: str,
):
    """Parse client side encryption configuration."""
    if len(data) > 1:
        raise ConfigParsingError(
            f"Only one client side encryption type can be used for {cloud_provider}."
        )
    for key, config in supported_encryptions.items():
        if key in data:
            return config._from_dict(data[key])
    raise ConfigParsingError(
        f"Supported client side encryption types in {cloud_provider} are {supported_encryptions.keys()}"
    )
