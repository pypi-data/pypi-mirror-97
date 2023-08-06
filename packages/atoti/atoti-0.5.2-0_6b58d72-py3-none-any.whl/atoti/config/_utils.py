from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Any, Mapping, Type, TypeVar

from atoti.config.parsing import ConfigParsingError

from .._path_utils import get_atoti_home
from .._serialization_utils import FromDict
from .parsing import ConfigParsingError


def _get_default_config_path() -> Path:
    """Get the path to the default config."""
    return get_atoti_home() / "config.yml"


def defined_kwargs(**kwargs: Any) -> Any:
    return {k: v for k, v in kwargs.items() if v is not None}


_Config = TypeVar("_Config", bound="Configuration")


class Configuration(FromDict):
    @classmethod
    @abstractmethod
    def _create(cls: Type[_Config], data: Mapping[str, Any]) -> _Config:
        """Create the configuration without checking for type errors."""
        ...

    @classmethod
    def _from_dict(cls: Type[_Config], data: Mapping[str, Any]) -> _Config:
        try:
            return cls._create(data)
        except TypeError as error:
            raise ConfigParsingError(
                f"Failed to parse YAML configuration into {cls.__name__}: {error.args[0]}.\nUnderlying data is {data}"
            ) from error
