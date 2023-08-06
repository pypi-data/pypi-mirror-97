from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from ._bitwise_operators_only import BitwiseOperatorsOnly

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from ._measures.boolean_measure import BooleanMeasure
    from ._measures.calculated_measure import CalculatedMeasure
    from .cube import Cube


@dataclass(eq=False)
class Measure(BitwiseOperatorsOnly):
    """A measure is a mostly-numeric data value, computed on demand for aggregation purposes.

    Measures can be compared to other objects, such as a literal value, a :class:`~atoti.level.Level`, or another measure.
    The returned measure represents the outcome of the comparison and this measure can be used as a condition.
    If the measure's value is ``None`` when evaluating a conditon, the returned value will be ``False``.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Id", "Value", "Threshold"],
        ...     data=[
        ...         (0, 1.0, 5.0),
        ...         (1, 2.0, None),
        ...         (2, 3.0, 3.0),
        ...         (3, 4.0, None),
        ...         (4, 5.0, 1.0),
        ...     ],
        ... )
        >>> store = session.read_pandas(df, keys=["Id"], store_name="Measure example")
        >>> cube = session.create_cube(store)
        >>> lvl, m = cube.levels, cube.measures
        >>> m["Condition"] = m["Value.SUM"] > m["Threshold.SUM"]
        >>> cube.query(m["Condition"], levels=lvl["Id"])
           Condition
        Id
        0      False
        1      False
        2      False
        3      False
        4       True

    """

    def _distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        """Return the name of the measure, creating it in the cube if it does not exist yet."""
        if not hasattr(self, "name"):
            self.name = (  # pylint: disable=attribute-defined-outside-init
                self._do_distil(java_api, cube, measure_name)
            )
        elif measure_name is not None:
            # This measure has already been distilled, this is a copy.
            java_api.copy_measure(cube.name, self, measure_name)
        return self.name

    @abstractmethod
    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        """Create the measure in the cube and return its name."""

    def __mul__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self * other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.mul([self, other_measure]))

    def __rmul__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other * self."""
        other_measure = _convert_to_measure(other)
        return self.__mul__(other_measure)

    def __truediv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self / other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.truediv([self, other_measure]))

    def __rtruediv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other / self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure(other)
        return CalculatedMeasure(Operator.truediv([other, self]))

    def __floordiv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self // other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure(other)
        return CalculatedMeasure(Operator.floordiv([self, other]))

    def __rfloordiv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other // self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure(other)
        return CalculatedMeasure(Operator.floordiv([other, self]))

    def __add__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self + other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.add([self, other_measure]))

    def __radd__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other + self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.add([other_measure, self]))

    def __sub__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self - other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.sub([self, other_measure]))

    def __rsub__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other - self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator.sub([other_measure, self]))

    def __pow__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self ** other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator("pow", [self, other_measure]))

    def __neg__(self) -> CalculatedMeasure:
        """Return a measure equal to -self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        return CalculatedMeasure(Operator.neg(self))

    def __mod__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self % other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure(other)
        return CalculatedMeasure(Operator("mod", [self, other_measure]))

    ########################
    # Boolean calculations #
    ########################

    def _boolean_calculation(self, other: Any, operation: str) -> BooleanMeasure:
        from ._measures.boolean_measure import BooleanMeasure

        other_measure = _convert_to_measure(other)
        return BooleanMeasure(operation, [self, other_measure])

    def __lt__(self, other: Any) -> BooleanMeasure:
        """Lower than operator."""
        return self._boolean_calculation(other, "lt")

    def __le__(self, other: Any) -> BooleanMeasure:
        """Lower or equal operator."""
        return self._boolean_calculation(other, "le")

    def __gt__(self, other: Any) -> BooleanMeasure:
        """Greater than operator."""
        return self._boolean_calculation(other, "gt")

    def __ge__(self, other: Any) -> BooleanMeasure:
        """Greater or equal operator."""
        return self._boolean_calculation(other, "ge")

    def __eq__(self, other: Any) -> BooleanMeasure:
        """Equals operator."""
        from ._measures.boolean_measure import BooleanMeasure

        if other is None:
            return BooleanMeasure("isNull", [self])
        return self._boolean_calculation(other, "eq")

    def __ne__(self, other: Any) -> BooleanMeasure:
        """Not equals operator."""
        from ._measures.boolean_measure import BooleanMeasure

        if other is None:
            return BooleanMeasure("notNull", [self])
        return self._boolean_calculation(other, "ne")

    ####################
    # Array operations #
    ####################

    def __getitem__(self, key: Union[slice, int, MeasureLike]) -> Measure:
        """Return a measure equal to the element or slice of this array measure at the passed index(es)."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        # Return a sub-vector if the key is a slice.
        # Because MeasureLike is unbound, pyright throws an error here
        if isinstance(key, slice):
            if key.step:
                raise ValueError("step cannot be used to slice an array measure.")
            start = key.start if key.start is not None else float("nan")
            stop = key.stop if key.stop is not None else float("nan")
            return CalculatedMeasure(
                Operator(
                    "vector_sub",
                    [self, _convert_to_measure(start), _convert_to_measure(stop)],
                )
            )

        # Return a single element.
        if isinstance(key, (int, Measure, MeasureConvertible)):
            return CalculatedMeasure(
                Operator("vector_element", [self, _convert_to_measure(key)])
            )

        # Crappy input
        raise TypeError("The index must be a slice, a measure or an integer")

    def _get_bool_alternative_message(self) -> str:  # pylint: disable=no-self-use
        return "For conditions on measure values use `where` or `filter` method."


class MeasureConvertible(BitwiseOperatorsOnly):
    """Instances of this class can be converted to measures."""

    @abstractmethod
    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        """Convert this object into a measure.

        Args:
            agg_fun: The aggregation function.
        """


LiteralMeasureValue = Union[date, datetime, int, float, str, List[int], List[float]]
MeasureLike = Union[LiteralMeasureValue, Measure, MeasureConvertible]


def _convert_to_measure(arg: MeasureLike) -> Measure:
    """Convert the passed argument to a measure."""
    from ._measures.literal_measure import LiteralMeasure

    if arg is None:
        raise ValueError("None cannot be converted to a measure.")
    if isinstance(arg, Measure):
        return arg
    if isinstance(arg, MeasureConvertible):
        return arg._to_measure()
    return LiteralMeasure(arg)
