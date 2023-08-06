"""Module for partial aggregate providers.

These are optimizations to pre-aggregate some store columns up to certain levels.
One can choose the levels and the measures (among store aggregations) to build the provider on.
If a step of a query uses a subset of the aggregate provider's levels and measures it can use this provider and speed up the query.

Aggregate providers will use additional memory to store the intermediate aggregates,
the more levels and measures are added the more memory it requires.

There are actually two kinds of aggregate providers: the bitmap and the leaf.
The bitmap is generally faster but also takes more memory.
"""

from dataclasses import dataclass
from typing import List

from ..level import Level
from ..measures import NamedMeasure

_BITMAP_KEY = "BITMAP"
_LEAF_KEY = "LEAF"


@dataclass(frozen=True)
class PartialAggregateProvider:
    """Partial Aggregate Provider."""

    key: str
    levels: List[Level]
    measures: List[NamedMeasure]

    def __repr__(self) -> str:
        """Get the string representation."""
        return (
            self.key
            + "(levels=["
            + ", ".join([lvl.name for lvl in self.levels])
            + "], measures=["
            + ",".join([measure.name for measure in self.measures])
            + "])"
        )

    def __eq__(self, o: object) -> bool:  # pylint: disable=too-many-return-statements
        # This is needed since vcomparing two levels or measures with == return a condition, the default eq does not work here.
        if not isinstance(o, PartialAggregateProvider):
            return False
        if self.key != o.key:
            return False
        if len(self.measures) != len(o.measures):
            return False
        if len(self.levels) != len(o.levels):
            return False
        for i in range(len(self.measures)):
            if self.measures[i]._name != o.measures[i]._name:
                return False
        for i in range(len(self.levels)):
            if self.levels[i]._java_description != o.levels[i]._java_description:
                return False
        return True


def bitmap(
    *, levels: List[Level], measures: List[NamedMeasure]
) -> PartialAggregateProvider:
    """Create a partial bitmap aggregate provider.

    Args:
        levels: The levels to build the bitmap provider on.
        measures: The measures to put in the bitmap provider.
    """
    return PartialAggregateProvider(_BITMAP_KEY, levels, measures)


def leaf(
    *, levels: List[Level], measures: List[NamedMeasure]
) -> PartialAggregateProvider:
    """Create a partial leaf aggregate provider.

    Args:
        levels: The levels to build the leaf provider on.
        measures: The measures to put in the leaf provider.
    """
    return PartialAggregateProvider(_LEAF_KEY, levels, measures)
