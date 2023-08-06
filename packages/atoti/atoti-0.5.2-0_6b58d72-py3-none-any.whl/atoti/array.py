from __future__ import annotations

from typing import Union

from ._docs_utils import (
    QUANTILE_DOC,
    QUANTILE_INDEX_DOC,
    STD_AND_VAR_DOC,
    STD_DOC_KWARGS,
    VAR_DOC_KWARGS,
    doc,
)
from ._measures.calculated_measure import CalculatedMeasure, Operator
from ._measures.generic_measure import GenericMeasure
from ._type_utils import (
    DataTypeError,
    PercentileIndexInterpolation,
    PercentileInterpolation,
    PercentileMode,
    VarianceMode,
)
from .math import sqrt
from .measure import Measure, _convert_to_measure
from .named_measure import NamedMeasure
from .type import _ARRAYS


def _check_array_type(measure: Measure):
    if isinstance(measure, NamedMeasure) and measure.data_type not in _ARRAYS:
        raise DataTypeError(measure, "array")


def sum(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the sum of all the elements of the passed array measure.

    The sum of an empty array is 0.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("sum_vector", [measure]))


def positive_values(measure: Measure) -> Measure:
    """Return a measure where all the elements < 0 of the passed array measure are replaced by 0."""
    _check_array_type(measure)
    return CalculatedMeasure(Operator("positive_vector", [measure]))


def negative_values(measure: Measure) -> Measure:
    """Return a measure where all the elements > 0 of the passed array measure are replaced by 0."""
    _check_array_type(measure)
    return CalculatedMeasure(Operator("negative_vector", [measure]))


def mean(measure: Measure) -> Measure:
    """Return a measure equal to the mean of all the elements of the passed array measure.

    The mean of an empty array is 0.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("mean_vector", [measure]))


def prod(measure: Measure) -> Measure:
    """Return a measure equal to the product of all the elements of the passed array measure.

    The product of an empty array is 1.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("product_vector", [measure]))


def min(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the minimum element of the passed array measure.

    The min of an empty array is ``None``.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("min_vector", [measure]))


def max(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the maximum element of the passed array measure.

    The max of an empty array is ``None``.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("max_vector", [measure]))


_QUANTILE_STD_AND_VAR_DOC_KWARGS = {
    "what": "of the elements of the passed array measure"
}


@doc(STD_AND_VAR_DOC, **{**VAR_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS})
def var(measure: Measure, *, mode: VarianceMode = "sample") -> Measure:
    _check_array_type(measure)
    return CalculatedMeasure(Operator("variance", [measure, mode]))


@doc(
    STD_AND_VAR_DOC,
    **{**STD_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS},
)
def std(measure: Measure, *, mode: VarianceMode = "sample") -> Measure:
    _check_array_type(measure)
    return sqrt(var(measure, mode=mode))


def sort(measure: Measure, *, ascending: bool = True) -> Measure:
    """Return an array measure with the elements of the passed array measure sorted.

    Args:
        measure: The array measure to sort.
        ascending: When set to ``False``, the first value will be the greatest.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("sort", [measure, str(ascending)]))


@doc(QUANTILE_DOC, **_QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile(
    measure: Measure,
    q: Union[float, Measure],
    *,
    mode: PercentileMode = "inc",
    interpolation: PercentileInterpolation = "linear",
) -> Measure:
    if isinstance(q, float):
        if q < 0 or q > 1:
            raise ValueError("Quantile must be between 0 and 1.")
    elif not isinstance(q, Measure):
        raise TypeError("The quantile must be a measure or a float.")
    _check_array_type(measure)
    return GenericMeasure(
        "CALCULATED_QUANTILE", mode, interpolation, [measure, _convert_to_measure(q)]
    )


@doc(QUANTILE_INDEX_DOC, **_QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile_index(
    measure: Measure,
    q: Union[float, Measure],
    *,
    mode: PercentileMode = "inc",
    interpolation: PercentileIndexInterpolation = "lower",
) -> Measure:
    if isinstance(q, float):
        if q < 0 or q > 1:
            raise ValueError("Quantile must be between 0 and 1.")
    elif not isinstance(q, Measure):
        raise TypeError("The quantile must be a measure or a float.")
    _check_array_type(measure)
    return GenericMeasure(
        "CALCULATED_QUANTILE_INDEX",
        mode,
        interpolation,
        [measure, _convert_to_measure(q)],
    )


def _validate_n_param(n: Union[int, Measure]):
    if isinstance(n, int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")
    elif not isinstance(n, Measure):
        raise TypeError("n must be a measure or an int.")


def n_lowest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the ``n`` lowest elements of the passed array measure."""
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(Operator("n_lowest", [measure, _convert_to_measure(n)]))


def n_lowest_indices(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the indices of the ``n`` lowest elements of the passed array measure.

    Example:
        The following example creates a measure that returns the 3 lowest indices of an array::

            m["array"] = [ 400, 200, 100, 500, 300]
            m["3 lowest indices"] = atoti.array.n_lowest_indices(m["array"], 3)

        This measure will return ``[2, 1, 4]`` because the lowest values are ``100`` at index 2, then ``200`` at index 1 and ``300`` at index 4.

    """
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(
        Operator("n_lowest_indices", [measure, _convert_to_measure(n)])
    )


def nth_lowest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return a measure equal to the ``n``-th lowest element of the passed array measure."""
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(Operator("nth_lowest", [measure, _convert_to_measure(n)]))


def n_greatest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the ``n`` greatest elements of the passed array measure."""
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(Operator("n_greatest", [measure, _convert_to_measure(n)]))


def n_greatest_indices(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the indices of the ``n`` greatest elements of the passed array measure.

    Example:
        The following example creates a measure that returns the 3 greatest indices of an array::

            m["array"] = [ 400, 200, 100, 500, 300]
            m["3 greatest indices"] = atoti.array.n_greatest_indices(m["array"], 3)

        This measure will return ``[3, 0, 4]`` because the greatest values are ``500`` at index 3, then ``400`` at index 0 and ``300`` at index 4.

    """
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(
        Operator("n_greatest_indices", [measure, _convert_to_measure(n)])
    )


def nth_greatest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return a measure equal to the ``n``-th greatest element of the passed array measure."""
    _validate_n_param(n)
    _check_array_type(measure)
    return CalculatedMeasure(
        Operator("nth_greatest", [measure, _convert_to_measure(n)])
    )


def len(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the number of elements of the passed array measure."""
    _check_array_type(measure)
    return CalculatedMeasure(Operator("vector_length", [measure]))


def prefix_sum(measure: Measure) -> Measure:
    """Return a measure equal to the sum of the previous elements in the passed array measure.

    Example:
        If an array has the following values: ``[2.0, 1.0, 0.0, 3.0]``, the returned array will be: ``[2.0, 3.0, 3.0, 6.0]``.
    """
    _check_array_type(measure)
    return CalculatedMeasure(Operator("prefix_sum", [measure]))
