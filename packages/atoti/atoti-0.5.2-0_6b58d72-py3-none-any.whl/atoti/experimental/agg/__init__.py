from __future__ import annotations

from typing import Optional

from ...agg import MeasureOrMeasureConvertible, _agg  # pylint: disable=protected-access
from ...measure import Measure
from ...scope.scope import Scope


def distinct(
    measure: MeasureOrMeasureConvertible, *, scope: Optional[Scope] = None
) -> Measure:
    """Return an array measure representing the distinct values of the passed measure."""
    return _agg("DISTINCT", measure=measure, scope=scope)
