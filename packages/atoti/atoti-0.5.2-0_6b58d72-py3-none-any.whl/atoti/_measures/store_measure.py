from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Collection, Optional

from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..level import Level
    from ..store import Column, Store


@dataclass(eq=False)
class StoreMeasure(Measure):
    """Measure based on the column of a store."""

    _column: Column
    _agg_fun: str
    _store: Store = field(repr=False)

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        return java_api.aggregated_measure(
            cube, measure_name, self._store.name, self._column.name, self._agg_fun, []
        )


@dataclass(eq=False)
class SingleValueStoreMeasure(Measure):
    """Single value aggregated measure based on the column of a store."""

    _column: Column
    _levels: Optional[Collection[Level]] = None

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        store = self._column._store  # pylint: disable=protected-access
        # levels = [] if self._levels is None else self._levels

        distilled_name = java_api.aggregated_measure(
            cube,
            measure_name,
            store.name,
            self._column.name,
            "SINGLE_VALUE_NULLABLE",
            self._levels,
        )

        return distilled_name
