from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Mapping, TypeVar

from ._base._base_cubes import BaseCubes
from ._ipython_utils import ipython_key_completions_for_mapping
from ._local_cube import _LocalCube
from ._mappings import DelegateMutableMapping

if TYPE_CHECKING:
    from ._local_session import LocalSession

_LocalCubes = TypeVar("_LocalCubes", bound="LocalCubes")


@dataclass(frozen=True)
class LocalCubes(DelegateMutableMapping[str, _LocalCube], BaseCubes[_LocalCube]):
    """Local cubes class."""

    _session: LocalSession = field(repr=False)

    def __setitem__(self, key: str, value: _LocalCube) -> None:
        """Set the cube for the given name."""
        raise RuntimeError(
            "Cannot set cube directly. Use session.create_cube() instead."
        )

    # pylint: disable=protected-access

    def __delitem__(self, key: str) -> None:
        """Delete the cube with the given name."""
        try:
            self._session._java_api.delete_cube(key)
            self._session._java_api.refresh_pivot()
        except KeyError:
            raise Exception(f"No cube named {key}") from None

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self)

    @staticmethod
    def _retrieve_cubes(session: LocalSession[Any]) -> Mapping[str, _LocalCube]:
        return session._java_api.retrieve_cubes(session)

    @staticmethod
    def _retrieve_cube(cube_name: str, session: LocalSession[Any]) -> _LocalCube:
        return session._java_api.retrieve_cube(cube_name, session)

    # pylint: enable=protected-access
