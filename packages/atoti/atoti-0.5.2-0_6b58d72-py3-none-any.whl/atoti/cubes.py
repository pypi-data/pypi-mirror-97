from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping

from ._local_cubes import LocalCubes
from .cube import Cube

if TYPE_CHECKING:
    from .session import Session


@dataclass(frozen=True)
class Cubes(LocalCubes[Cube]):
    """Manage the cubes of the session."""

    _session: Session = field(repr=False)

    def _get_underlying(self) -> Mapping[str, Cube]:
        return self._retrieve_cubes(self._session)

    def __getitem__(self, key: str) -> Cube:
        """Get the cube with the given name."""
        return self._retrieve_cube(key, self._session)
