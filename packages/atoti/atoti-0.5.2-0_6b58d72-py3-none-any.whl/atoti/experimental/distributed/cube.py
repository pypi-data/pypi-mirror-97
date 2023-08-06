from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Mapping

from ..._local_cube import LocalCube
from ...aggregates_cache import AggregatesCache
from ...query._cellset import LevelCoordinates
from .hierarchies import DistributedHierarchies
from .levels import DistributedLevels
from .measures import DistributedMeasures

if TYPE_CHECKING:
    from ..._java_api import JavaApi
    from .session import DistributedSession


class DistributedCube(
    LocalCube[DistributedHierarchies, DistributedLevels, DistributedMeasures]
):
    """Cube of a distributed session."""

    def __init__(self, java_api: JavaApi, name: str, session: DistributedSession):
        """Init."""
        super().__init__(
            name,
            java_api,
            session,
            DistributedHierarchies(java_api, self),
            lambda hierarchies: DistributedLevels(hierarchies),
            DistributedMeasures(java_api, self),
            AggregatesCache(java_api, self),
        )

    def _get_level_data_types(  # pylint: disable=no-self-use
        self, levels_coordinates: Collection[LevelCoordinates]
    ) -> Mapping[LevelCoordinates, str]:
        return {level_coordinates: "object" for level_coordinates in levels_coordinates}
