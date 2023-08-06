from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict

from atoti.query.measure import QueryMeasure

from ..._local_measures import LocalMeasures
from ...exceptions import AtotiJavaException
from ...measure import MeasureLike

if TYPE_CHECKING:
    from ..._java_api import JavaApi
    from .cube import DistributedCube


@dataclass(init=False)
class DistributedMeasures(LocalMeasures[QueryMeasure]):
    """Manage the measures."""

    def __init__(self, java_api: JavaApi, cube: DistributedCube = field(repr=False)):
        super().__init__(java_api)
        self._cube = cube

    def _get_underlying(self) -> Dict[str, QueryMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_full_measures(self._cube)
        return {
            name: QueryMeasure(
                name,
                cube_measures[name].visible,
                cube_measures[name].folder,
                cube_measures[name].formatter,
                cube_measures[name].description,
            )
            for name in cube_measures
        }

    def __getitem__(self, key: str) -> QueryMeasure:
        """Return the measure with the given name."""
        try:
            cube_measure = self._java_api.get_measure(self._cube, key)
            return QueryMeasure(
                key,
                cube_measure.visible,
                cube_measure.folder,
                cube_measure.formatter,
                cube_measure.description,
            )
        except AtotiJavaException:
            raise KeyError(f"No measure named {key}") from None

    def __setitem__(self, key: str, value: MeasureLike) -> None:
        raise NotImplementedError("Distributed cube measures cannot be changed")

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Distributed cube measures cannot be changed")
