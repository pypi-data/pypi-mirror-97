from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union

from ._measures.store_measure import SingleValueStoreMeasure, StoreMeasure
from ._operation import ColumnOperation, Operation
from .measure import Measure, MeasureConvertible
from .type import DataType

if TYPE_CHECKING:
    from .store import Store

# Type for store rows
Row = Union[Tuple[Any, ...], Dict[str, Any]]


@dataclass(frozen=True)
class Column(MeasureConvertible):
    """Column of a Store."""

    name: str
    """The name of the column."""

    data_type: DataType
    """The type of the elements in the column."""

    _store: Store = field(repr=False)

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        """Convert this column into a measure.

        If no aggregation function is given, it becomes a lookup measure.
        Otherwise a regular aggregated measure.

        Args:
            agg_fun: The aggregation function.

        """
        return (
            StoreMeasure(self, agg_fun, self._store)
            if agg_fun
            else SingleValueStoreMeasure(self)
        )

    def __mul__(self, other: Any) -> Operation:
        """Multiplication operator."""
        return ColumnOperation(self) * other

    def __rmul__(self, other: Any) -> Operation:
        """Multiplication operator."""
        return other * ColumnOperation(self)

    def __truediv__(self, other: Any) -> Operation:
        """Division operator."""
        return ColumnOperation(self) / other

    def __rtruediv__(self, other: Any) -> Operation:
        """Division operator."""
        return other / ColumnOperation(self)

    def __add__(self, other: Any) -> Operation:
        """Addition operator."""
        return ColumnOperation(self) + other

    def __radd__(self, other: Any) -> Operation:
        """Addition operator."""
        return other + ColumnOperation(self)

    def __sub__(self, other: Any) -> Operation:
        """Subtraction operator."""
        return ColumnOperation(self) - other

    def __rsub__(self, other: Any) -> Operation:
        """Subtraction operator."""
        return other - ColumnOperation(self)

    def __eq__(self, other: Any) -> Operation:
        """Equal operator."""
        return ColumnOperation(self) == other

    def __ne__(self, other: Any) -> Operation:
        """Not equal operator."""
        return ColumnOperation(self) != other

    def __lt__(self, other: Any) -> Operation:
        """Lower than operator."""
        return ColumnOperation(self) < other

    def __gt__(self, other: Any) -> Operation:
        """Greater than operator."""
        return ColumnOperation(self) > other

    def __le__(self, other: Any) -> Operation:
        """Lower than or equal operator."""
        return ColumnOperation(self) <= other

    def __ge__(self, other: Any) -> Operation:
        """Greater than or equal operator."""
        return ColumnOperation(self) >= other

    def _identity(self):
        return (
            self.name,
        ) + self._store._identity()  # pylint: disable=protected-access
