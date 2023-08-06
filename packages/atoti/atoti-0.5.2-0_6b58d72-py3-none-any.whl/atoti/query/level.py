from dataclasses import dataclass
from typing import Any

from .._base._base_level import BaseLevel
from .._level_conditions import LevelCondition
from .._repr_utils import ReprJson


@dataclass(eq=False)
class QueryLevel(BaseLevel):
    """Level of a query cube."""

    _dimension: str
    _hierarchy: str

    @property
    def dimension(self) -> str:
        return self._dimension

    @property
    def hierarchy(self) -> str:
        return self._hierarchy

    def __ne__(self, other: Any) -> LevelCondition:
        """Not supported."""
        # Explicitly implemented so that Python doesn't just silently return False.
        raise NotImplementedError(
            "Query level conditions can only be based on equality (==)."
        )

    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
        }
        return (
            data,
            {"expanded": True, "root": self.name},
        )
