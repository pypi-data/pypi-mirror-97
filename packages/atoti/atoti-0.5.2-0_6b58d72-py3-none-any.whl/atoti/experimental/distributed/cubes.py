from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping

from ..._local_cubes import LocalCubes
from .cube import DistributedCube

if TYPE_CHECKING:
    from .session import DistributedSession


@dataclass(frozen=True)
class DistributedCubes(LocalCubes[DistributedCube]):
    """Manage the distributed cubes."""

    _session: DistributedSession = field(repr=False)

    def _get_underlying(self) -> Mapping[str, DistributedCube]:
        return self._retrieve_cubes(self._session)

    def __getitem__(self, key: str) -> DistributedCube:
        """Get the cube with the given name."""
        return self._retrieve_cube(key, self._session)
