from __future__ import annotations

from typing import List, Optional, Union

from ._docs_utils import (
    QUANTILE_DOC,
    STD_AND_VAR_DOC,
    STD_DOC_KWARGS,
    VAR_DOC_KWARGS,
    doc,
)
from ._measures.calculated_measure import AggregatedMeasure
from ._measures.generic_measure import GenericMeasure
from ._measures.sum_product_measure import (
    SumProductEncapsulationMeasure,
    SumProductFieldsMeasure,
)
from ._type_utils import PercentileInterpolation, PercentileMode, VarianceMode
from .array import quantile as array_quantile
from .level import Level
from .math import sqrt
from .measure import Measure, MeasureConvertible
from .scope._utils import LeafLevels, Window
from .scope.scope import Scope
from .store import Column

MeasureOrMeasureConvertible = Union[Measure, MeasureConvertible]


_BASIC_DOC = """Return a measure equal to the {value} of the passed measure across the specified scope.

    {args}
"""

_SCOPE_DOC = """
        scope: The scope of the aggregation.
               When ``None`` is specified, the natural aggregation scope is used: it contains all the data in the cube which coordinates match the ones of the currently evaluated member.
    """
_BASIC_ARGS_DOC = (
    """
    Args:
        measure: The measure or store column to aggregate.
"""
    + _SCOPE_DOC
)

_QUANTILE_STD_AND_VAR_DOC_KWARGS = {
    "what": "of the passed measure across the specified scope",
}


def _agg(
    agg_fun: str,
    measure: Union[Measure, MeasureConvertible],
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    """Return a measure aggregating the passed one.

    A scope can only be specified when passing an instance of Measure.
    """
    if not isinstance(measure, Measure):
        if scope is not None:
            raise ValueError(
                (
                    """Illegal argument "scope" if you are not passing a measure object """
                    """as "measure" argument."""
                )
            )
        return measure._to_measure(agg_fun)

    if isinstance(scope, Window):
        return scope._create_aggregated_measure(  # pylint: disable=protected-access
            measure, agg_fun
        )
    if isinstance(scope, LeafLevels) or scope is None:
        return AggregatedMeasure(measure, agg_fun, scope)
    raise TypeError(f"Scope {scope} of invalid type {type(scope).__name__} passed")


def _stop(measure: Measure, *at: Level) -> Measure:
    """Return a measure equal to the passed measure at and below the given levels and ``None`` above them.

    Example:
        Consider the following measures::

            m["stop1"] = tt.agg.stop(m["Quantity"], lvl["Date"])
            m["stop2"] = tt.agg.stop(m["Quantity"], lvl["Date"], lvl["Product"])

        +-----+------------+---------+----------+-------+-------+
        |     | Date       | Product | Quantity | stop1 | stop2 |
        +=====+============+=========+==========+=======+=======+
        | ALL |            |         | 700      |       |       |
        +-----+------------+---------+----------+-------+-------+
        |     | 2020-01-01 |         | 400      | 400   |       |
        +-----+------------+---------+----------+-------+-------+
        |     |            | A       | 150      | 150   | 150   |
        +-----+------------+---------+----------+-------+-------+
        |     |            | B       | 250      | 250   | 250   |
        +-----+------------+---------+----------+-------+-------+
        |     | 2020-01-02 |         | 300      | 300   |       |
        +-----+------------+---------+----------+-------+-------+
        |     |            | A       | 200      | 200   | 200   |
        +-----+------------+---------+----------+-------+-------+
        |     |            | B       | 100      | 100   | 100   |
        +-----+------------+---------+----------+-------+-------+

        stop1 is only defined when the Date level is defined.
        stop2 is only defined when both the Date level and the Product level are defined.

    Args:
        measure: The measure to stop aggregating.
        at: One or more levels to stop at.
    """
    if not at:
        raise ValueError("Expected at least one level")

    return GenericMeasure("LEAF_NOAGG", measure, set(at))


def _count(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    """Return a measure equal to the number of aggregated elements.

    With a store column, it counts the number of facts.
    With a measure and a level, it counts the number of level members.
    To count the number of distinct elements, use :func:`atoti.agg.count_distinct`.
    """
    return _agg(agg_fun="COUNT", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="sum")
def sum(  # pylint: disable=redefined-builtin
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="SUM", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="product")
def prod(  # pylint: disable=redefined-builtin
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="MULTIPLY", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="mean")
def mean(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="MEAN", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="minimum")
def min(  # pylint: disable=redefined-builtin
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="MIN", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="maximum")
def max(  # pylint: disable=redefined-builtin
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="MAX", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="median")
def median(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return quantile(measure, q=0.5, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="sum of the square")
def square_sum(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="SQ_SUM", measure=measure, scope=scope)


@doc(
    STD_AND_VAR_DOC,
    _SCOPE_DOC,
    **{**VAR_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS},
)
def var(
    measure: MeasureOrMeasureConvertible,
    *,
    mode: VarianceMode = "sample",
    scope: Optional[Scope] = None,
) -> Measure:
    size = _count(measure, scope=scope)
    mean_value = mean(measure, scope=scope)
    population_var = square_sum(measure, scope=scope) / size - mean_value * mean_value
    if mode == "population":
        return population_var
    # Apply Bessel's correction
    return population_var * size / (size - 1)


@doc(
    STD_AND_VAR_DOC,
    _SCOPE_DOC,
    **{**STD_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS},
)
def std(
    measure: MeasureOrMeasureConvertible,
    *,
    mode: VarianceMode = "sample",
    scope: Optional[Scope] = None,
) -> Measure:
    return sqrt(var(measure, mode=mode, scope=scope))


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="sum of the negative values")
def short(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="SHORT", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="sum of the positive values")
def long(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    return _agg(agg_fun="LONG", measure=measure, scope=scope)


@doc(args=_BASIC_ARGS_DOC)
def _single_value(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    """Return a measure equal to the value aggregation of the passed measure across the specified scope.

    The new measure value is equal to the value of the aggregated elements if they are all equal, and to ``None`` otherwise.

    Example:
        Considering this dataset with, for each day and product, the sold amount and the product price:

        +------------+------------+----------+-------+--------+
        | Date       | Product ID | Category | Price | Amount |
        +============+============+==========+=======+========+
        | 2020-01-01 | 001        | TV       | 300.0 | 5.0    |
        +------------+------------+----------+-------+--------+
        | 2020-01-02 | 001        | TV       | 300.0 | 1.0    |
        +------------+------------+----------+-------+--------+
        | 2020-01-01 | 002        | Computer | 900.0 | 2.0    |
        +------------+------------+----------+-------+--------+
        | 2020-01-02 | 002        | Computer | 900.0 | 3.0    |
        +------------+------------+----------+-------+--------+
        | 2020-01-01 | 003        | TV       | 500.0 | 2.0    |
        +------------+------------+----------+-------+--------+

        As the price is constant for a product, ``value`` can be used to aggregate it::

            m["Product Price"] = atoti.agg.value(store["Price"])

        At the Product ID level, there is a single price so the aggregation forwards it::

            cube.query(m["Product Price"], levels=lvl["Product ID"])

        +------------+---------------+
        | Product ID | Product Price |
        +============+===============+
        | 001        | 300.0         |
        +------------+---------------+
        | 002        | 900.0         |
        +------------+---------------+
        | 003        | 500.0         |
        +------------+---------------+

        However, at the Category level, it behaves differently::

            cube.query(m["Product Price"], levels=lvl["Category"])

        +----------+---------------+
        | Category | Product Price |
        +==========+===============+
        | Computer | 900.0         |
        +----------+---------------+
        | TV       |               |
        +----------+---------------+

        * Computer: single price so the measure still forwards it.
        * TV: two different prices so the measure equals ``None``.

    {args}
    """
    return _agg(agg_fun="SINGLE_VALUE_NULLABLE", measure=measure, scope=scope)


@doc(_BASIC_DOC, args=_BASIC_ARGS_DOC, value="distinct count")
def count_distinct(
    measure: MeasureOrMeasureConvertible, *, scope: Optional[Scope] = None
) -> Measure:
    return _agg(agg_fun="DISTINCT_COUNT", measure=measure, scope=scope)


def _vector(
    measure: MeasureOrMeasureConvertible,
    *,
    scope: Optional[Scope] = None,
) -> Measure:
    """Return an array measure representing the values of the passed measure across the specified scope."""
    return _agg(agg_fun="VECTOR", measure=measure, scope=scope)


@doc(QUANTILE_DOC, _SCOPE_DOC, **_QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile(
    measure: MeasureOrMeasureConvertible,
    q: Union[float, Measure],
    *,
    mode: PercentileMode = "inc",
    interpolation: PercentileInterpolation = "linear",
    scope: Optional[Scope] = None,
) -> Measure:
    return array_quantile(
        _vector(measure, scope=scope), q=q, mode=mode, interpolation=interpolation
    )


_EXTREMUM_MEMBER_DOC = """Return a measure equal to the member {op}imizing the passed measure on the given level.

    When multiple members maximize the passed measure, the first one
    (according to the comparator of the given level) is returned.

    Example:
        Considering this dataset:

        +---------------+----------+-------+
        |   Continent   |   City   | Price |
        +===============+==========+=======+
        | Europe        | Paris    | 200.0 |
        +---------------+----------+-------+
        | Europe        | Berlin   | 150.0 |
        +---------------+----------+-------+
        | Europe        | London   | 240.0 |
        +---------------+----------+-------+
        | North America | New York | 270.0 |
        +---------------+----------+-------+

        And this measure::

            m["City with {op} price"] = atoti.agg.{op}_member(m["Price"], lvl["City"])

        Then, at the given level, the measure is equal to the current member of the City level::

            cube.query(m["Price"], m["City with {op} price"], levels=lvl["City"])

        +------------+-------+------------------------+
        |    City    | Price | City with {op} price    |
        +============+=======+========================+
        | Paris      | 200.0 | Paris                  |
        +------------+-------+------------------------+
        | Berlin     | 150.0 | Berlin                 |
        +------------+-------+------------------------+
        | London     | 240.0 | London                 |
        +------------+-------+------------------------+
        | New York   | 270.0 | New York               |
        +------------+-------+------------------------+

        At a level above it, the measure is equal to the city of each continent
        with the {op}imum price::

            cube.query(m["City with min price"], levels=lvl["Continent"])

       {continent_table}

        At the top level, the measure is equal to the city
        with the {op}ium price across all continents::

            cube.query(m["City with {op} price"])

        {top_level_table}

    Args:
        measure: The measure to {op}imize.
        level: The level on which the {op}imizing member is searched for.
"""


@doc(
    _EXTREMUM_MEMBER_DOC,
    op="max",
    continent_table="""
        +---------------+---------------------+
        |   Continent   | City with max price |
        +===============+=====================+
        | Europe        | London              |
        +---------------+---------------------+
        | North America | New York            |
        +---------------+---------------------+
""",
    top_level_table="""
        +---------------------+
        | City with max Price |
        +=====================+
        | New York            |
        +---------------------+
""",
)
def max_member(measure: MeasureOrMeasureConvertible, level: Level) -> Measure:
    if not isinstance(measure, Measure):
        measure = measure._to_measure()
    return GenericMeasure("COMPARABLE_MAX", measure, level, True, False)


@doc(
    _EXTREMUM_MEMBER_DOC,
    op="min",
    continent_table="""
        +---------------+---------------------+
        |   Continent   | City with min price |
        +===============+=====================+
        | Europe        | Berlin              |
        +---------------+---------------------+
        | North America | New York            |
        +---------------+---------------------+
""",
    top_level_table="""
        +---------------------+
        | City with min Price |
        +=====================+
        | Berlin              |
        +---------------------+
""",
)
def min_member(measure: MeasureOrMeasureConvertible, level: Level):
    if not isinstance(measure, Measure):
        measure = measure._to_measure()
    return GenericMeasure("COMPARABLE_MAX", measure, level, False, False)


@doc(_SCOPE_DOC)
def sum_product(
    *factors: MeasureOrMeasureConvertible,
    scope: Optional[Scope] = None,
) -> Measure:
    """Return a measure equal to the sum product aggregation of the passed factors across the specified scope.

    Example:
        Considering this dataset with, for each day and product, the sold amount and
        the product price:

        +------------+------------+----------+-------+--------+---------+
        | Date       | Product ID | Category | Price | Amount | Array   |
        +============+============+==========+=======+========+=========+
        | 2020-01-01 | 001        | TV       | 300.0 | 5.0    | [10,15] |
        +------------+------------+----------+-------+--------+---------+
        | 2020-01-02 | 001        | TV       | 200.0 | 1.0    | [5,15]  |
        +------------+------------+----------+-------+--------+---------+
        | 2020-01-01 | 002        | Computer | 900.0 | 2.0    | [2,3]   |
        +------------+------------+----------+-------+--------+---------+
        | 2020-01-02 | 002        | Computer | 800.0 | 3.0    | [10,20] |
        +------------+------------+----------+-------+--------+---------+
        | 2020-01-01 | 003        | TV       | 500.0 | 2.0    | [3,10]  |
        +------------+------------+----------+-------+--------+---------+

        To compute the turnover::

            m["turnover"] = atoti.agg.sum_product(store["Price"], store["Amount"])

        To compute the turnover per category::

            cube.query(m["turnover"], levels=["Category"])

        It returns:

        +------------+------------+
        | Category   | turnover   |
        +============+============+
        | TV         | 2700       |
        +------------+------------+
        | Computer   | 4200       |
        +------------+------------+

        Sum product is also optimized for operations on vectors::

            m["array sum product"] = atoti.agg.sum_product(store["Amount"], store["Array"])

        `cube.query(m["array sum product"])` return [95.0, 176.0]


    Args:
        factors: Column, Measure or Level to do the sum product of.
    """
    if len(factors) < 1:
        raise ValueError("At least one factor is needed")
    # pyright does not know there ris only columns in factors so we build a new sequence.
    factors_column: List[Column] = []
    for factor in factors:
        if isinstance(factor, Column):
            factors_column.append(factor)
    # Case with store fields
    if len(factors_column) == len(factors):
        if scope is None:
            return SumProductFieldsMeasure(factors_column)
        raise ValueError(
            "Scope is defined for store columns aggregation. "
            + "Scope must not be defined since this aggregation will be done at fact level."
        )
    # Otherwise case with two measures.
    return _agg(
        "SUM_PRODUCT",
        SumProductEncapsulationMeasure(
            [
                factor if isinstance(factor, Measure) else factor._to_measure()
                for factor in factors
            ]
        ),
        scope=scope,
    )
