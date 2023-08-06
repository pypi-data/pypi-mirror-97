from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ._base._base_level import BaseLevel
from ._level_conditions import LevelCondition
from ._repr_utils import ReprJson
from .comparator import Comparator
from .measure import Measure, MeasureConvertible
from .type import DataType

if TYPE_CHECKING:
    from .hierarchy import Hierarchy


@dataclass(eq=False)
class Level(BaseLevel, MeasureConvertible):
    """Level of a Hierarchy."""

    _column_name: str
    _data_type: DataType
    _hierarchy: Optional[Hierarchy] = None
    _comparator: Optional[Comparator] = None

    @property
    def dimension(self) -> str:
        """Name of the dimension holding the level."""
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        return self._hierarchy.dimension

    @property
    def hierarchy(self) -> str:
        """Name of the hierarchy holding the level."""
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        return self._hierarchy.name

    @property
    def data_type(self) -> DataType:
        """Type of the level members."""
        return self._data_type

    @property
    def comparator(self) -> Optional[Comparator]:  # noqa: D401
        """Comparator of the level."""
        return self._comparator

    @comparator.setter
    def comparator(self, value: Optional[Comparator]):  # noqa: D401
        """Comparator setter."""
        # pylint: disable=protected-access
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        self._comparator = value
        self._hierarchy._java_api.update_level_comparator(self)
        self._hierarchy._java_api.refresh_pivot()

    # pylint: disable=unused-argument
    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        """Convert this column into a measure."""
        from ._measures.level_measure import LevelMeasure

        if agg_fun is not None:
            from ._measures.calculated_measure import AggregatedMeasure
            from .scope import LeafLevels

            return AggregatedMeasure(LevelMeasure(self), agg_fun, LeafLevels([self]))
        return LevelMeasure(self)

    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
            "type": str(self.data_type),
        }
        if self.comparator is not None:
            data[
                "comparator"
            ] = self.comparator._name  # pylint: disable=protected-access
        return (data, {"expanded": True, "root": self.name})

    def __ne__(self, other: Any) -> LevelCondition:
        """Return a non-equality condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "ne")

    def __lt__(self, other: Any) -> LevelCondition:
        """Return a less than condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "lt")

    def __le__(self, other: Any) -> LevelCondition:
        """Return a less or equals condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "le")

    def __gt__(self, other: Any) -> LevelCondition:
        """Return a greater than condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "gt")

    def __ge__(self, other: Any) -> LevelCondition:
        """Return a greater or equal condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "ge")
