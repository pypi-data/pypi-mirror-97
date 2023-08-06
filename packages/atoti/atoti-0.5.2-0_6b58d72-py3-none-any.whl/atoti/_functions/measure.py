from __future__ import annotations

import warnings
from typing import Collection, Optional, Union

import typeguard

from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._measures.boolean_measure import BooleanMeasure
from .._measures.filtered_measure import LevelValueFilteredMeasure, WhereMeasure
from .._measures.generic_measure import GenericMeasure
from .._measures.store_measure import SingleValueStoreMeasure
from .._multi_condition import MultiCondition
from .._type_utils import DataTypeError, typecheck_ignore
from ..column import Column
from ..hierarchy import Hierarchy
from ..level import Level
from ..measure import Measure, MeasureLike, _convert_to_measure
from ..named_measure import NamedMeasure
from ..type import BOOLEAN, NULLABLE_BOOLEAN


def value(column: Column, *, levels: Optional[Collection[Level]] = None) -> Measure:
    """Return a measure equal to the value of the given store column.

    Args:
        column: The store column to get the value from.
        levels: The levels that must be expressed for this measure to possibly be non-null.

            When ``None``, the measure will also be ``None`` if the levels corresponding to the keys of ``column``'s store are not expressed.

            Passing an empty collection propagate the value on all levels when possible.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Month", "City", "Product", "Price"],
        ...     data=[
        ...         ("January", "Manchester", "Pretzel", 10.0),
        ...         ("January", "London", "Pretzel", 10.0),
        ...         ("January", "London", "Burger", 10.0),
        ...         ("March", "New York", "Pretzel", 10.0),
        ...         ("March", "New York", "Burger", 8.0),
        ...     ],
        ... )
        >>> store = session.read_pandas(
        ...     df, keys=["Month", "City", "Product"], store_name="value example"
        ... )
        >>> cube = session.create_cube(store)
        >>> lvl, m = cube.levels, cube.measures
        >>> m["Product Price"] = tt.value(store["Price"])

        By default, the values do not propagate:

        >>> cube.query(
        ...     m["Product Price"],
        ...     m["contributors.COUNT"],
        ...     include_totals=True,
        ...     levels=[lvl["Month"], lvl["City"], lvl["Product"]],
        ... )
                                   Product Price contributors.COUNT
        Month   City       Product
        Total                                                     5
        January                                                   3
                London                                            2
                           Burger          10.00                  1
                           Pretzel         10.00                  1
                Manchester                                        1
                           Pretzel         10.00                  1
        March                                                     2
                New York                                          2
                           Burger           8.00                  1
                           Pretzel         10.00                  1

        To propagate the values to the :guilabel:`City` level, the measure can instead be defined as follows:

        >>> m["Product Price"] = tt.value(store["Price"], levels=[lvl["City"]])

        With this definition, if all products of a city share the same price, then the city inherits that price:

        >>> cube.query(
        ...     m["Product Price"],
        ...     m["contributors.COUNT"],
        ...     include_totals=True,
        ...     levels=[lvl["Month"], lvl["City"], lvl["Product"]],
        ... )
                                   Product Price contributors.COUNT
        Month   City       Product
        Total                                                     5
        January                                                   3
                London                     10.00                  2
                           Burger          10.00                  1
                           Pretzel         10.00                  1
                Manchester                 10.00                  1
                           Pretzel         10.00                  1
        March                                                     2
                New York                                          2
                           Burger           8.00                  1
                           Pretzel         10.00                  1

        Since the measure has not been defined to propagate on :guilabel:`Product`, changing the order of the levels prevents any propagation:

        >>> cube.query(
        ...     m["Product Price"],
        ...     m["contributors.COUNT"],
        ...     include_totals=True,
        ...     levels=[lvl["Month"], lvl["Product"], lvl["City"]],
        ... )
                                   Product Price contributors.COUNT
        Month   Product City
        Total                                                     5
        January                                                   3
                Burger                                            1
                        London             10.00                  1
                Pretzel                                           2
                        London             10.00                  1
                        Manchester         10.00                  1
        March                                                     2
                Burger                                            1
                        New York            8.00                  1
                Pretzel                                           1
                        New York           10.00                  1

        Finally, using ``levels=[]``, the value propagates to :guilabel:`Month` too:

        >>> m["Product Price"] = tt.value(store["Price"], levels=[])
        >>> cube.query(
        ...     m["Product Price"],
        ...     m["contributors.COUNT"],
        ...     include_totals=True,
        ...     levels=[lvl["Month"], lvl["City"], lvl["Product"]],
        ... )
                                   Product Price contributors.COUNT
        Month   City       Product
        Total                                                     5
        January                            10.00                  3
                London                     10.00                  2
                           Burger          10.00                  1
                           Pretzel         10.00                  1
                Manchester                 10.00                  1
                           Pretzel         10.00                  1
        March                                                     2
                New York                                          2
                           Burger           8.00                  1
                           Pretzel         10.00                  1

    """
    return SingleValueStoreMeasure(column, levels)


@typecheck_ignore  # type checking is performed within the function
def filter(  # pylint: disable=redefined-builtin
    measure: MeasureLike,
    condition: Union[
        LevelCondition, MultiCondition, LevelIsInCondition, HierarchyIsInCondition
    ],
) -> Measure:
    """Return a filtered measure.

    The new measure is equal to the passed one where the condition is ``True`` and to ``None`` elsewhere.

    Different types of conditions are supported:

    * Levels compared to literals of the same type::

        lvl["city"] == "Paris"
        lvl["date"] > datetime.date(2020,1,1)
        lvl["age"] <= 18

    * A conjunction of conditions using the ``&`` operator::

        (lvl["source"] == lvl["destination"]) & (lvl["city"] == "Paris")

    Args:
        measure: The measure to filter.
        condition: The condition to evaluate.

    """
    measure = _convert_to_measure(measure)
    if isinstance(condition, BooleanMeasure):
        raise ValueError("Use atoti.where() for conditions with measures.")

    if isinstance(condition, LevelCondition):
        if isinstance(condition._value, Level):  # pylint: disable=protected-access
            warnings.warn(
                "Using a condition between two levels in atoti.filter() is deprecated",
                category=FutureWarning,
                stacklevel=2,
            )
        return LevelValueFilteredMeasure(measure, _level_conditions=[condition])

    if isinstance(condition, LevelIsInCondition):
        return LevelValueFilteredMeasure(measure, _level_isin_conditions=[condition])

    if isinstance(condition, HierarchyIsInCondition):
        return LevelValueFilteredMeasure(
            measure, _hierarchy_isin_conditions=[condition]
        )

    # Perform type checking after manual validation.
    typeguard.check_argument_types()

    # We only allow the use of level conditions
    if condition._measure_conditions:  # pylint: disable=protected-access
        raise ValueError("Use atoti.where() for conditions with measures.")

    # pylint: disable=protected-access
    return LevelValueFilteredMeasure(
        measure,
        condition._level_conditions if condition._level_conditions else None,
        condition._level_isin_conditions if condition._level_isin_conditions else None,
        condition._hierarchy_isin_condition
        if condition._hierarchy_isin_condition
        else None,
    )


def where(
    condition: Union[
        BooleanMeasure,
        LevelCondition,
        MultiCondition,
        HierarchyIsInCondition,
        LevelIsInCondition,
        NamedMeasure,
    ],
    true_measure: MeasureLike,
    # Not keyword-only to be symmetrical with true_measure and because
    # there probably will not be more optional parameters.
    false_measure: Optional[MeasureLike] = None,
) -> Measure:
    """Return a conditional measure.

    This function is like an *if-then-else* statement:

    * Where the condition is ``True``, the new measure will be equal to ``true_measure``.
    * Where the condition is ``False``, the new measure will be equal to ``false_measure``.

    If one of the values compared in the condition is ``None``, the condition will be considered ``False``.

    Different types of conditions are supported:

    * Measures compared to anything measure-like::

        m["Test"] == 20

    * Levels compared to levels, (if the level is not expressed, it is considered ``None``)::

        lvl["source"] == lvl["destination"]

    * Levels compared to literals of the same type::

        lvl["city"] == "Paris"
        lvl["date"] > datetime.date(2020,1,1)
        lvl["age"] <= 18

    * A conjunction or disjunction of conditions using the ``&`` operator or ``|`` operator::

        (m["Test"] == 20) & (lvl["city"] == "Paris")
        (lvl["Country"] == "USA") | (lvl["Currency"] == "USD")

    Args:
        condition: The condition to evaluate.
        true_measure: The measure to propagate where the condition is ``True``.
        false_measure: The measure to propagate where the condition is ``False``.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Id", "City", "Value"],
        ...     data=[
        ...         (0, "Paris", 1.0),
        ...         (1, "Paris", 2.0),
        ...         (2, "London", 3.0),
        ...         (3, "London", 4.0),
        ...         (4, "Paris", 5.0),
        ...     ],
        ... )
        >>> store = session.read_pandas(df, keys=["Id"], store_name="filter example")
        >>> cube = session.create_cube(store)
        >>> lvl, m = cube.levels, cube.measures
        >>> m["Paris value"] = tt.where(lvl["City"] == "Paris", m["Value.SUM"], 0)
        >>> cube.query(m["Paris value"], levels=lvl["City"])
               Paris value
        City
        London         .00
        Paris         8.00

    """
    # Collect the measure conditions.
    measure_conditions = []

    if isinstance(condition, BooleanMeasure):
        measure_conditions.append(condition)

    elif isinstance(
        condition, (LevelCondition, HierarchyIsInCondition, LevelIsInCondition)
    ):
        measure_conditions.append(condition._to_measure())

    elif isinstance(condition, NamedMeasure):
        if condition.data_type in [
            BOOLEAN,
            NULLABLE_BOOLEAN,
        ]:
            measure_conditions.append(condition)
        else:
            raise DataTypeError(condition, "boolean")

    elif isinstance(condition, MultiCondition):
        # condition._... is empty nothing happen
        measure_conditions.extend(
            [
                level_condition._to_measure()
                for level_condition in condition._level_conditions  # pylint: disable=protected-access
            ]
            + [
                hierarchy_isin_condition._to_measure()
                for hierarchy_isin_condition in condition._hierarchy_isin_condition  # pylint: disable=protected-access
            ]
            + [
                level_isin_condition._to_measure()
                for level_isin_condition in condition._level_isin_conditions  # pylint: disable=protected-access
            ]
            + list(condition._measure_conditions)  # pylint: disable=protected-access
        )

    else:
        raise ValueError(
            "Incorrect condition type."
            f" Expected {Union[BooleanMeasure, LevelCondition, MultiCondition, NamedMeasure]}"
            f" but got {type(condition)}."
        )

    return WhereMeasure(
        _convert_to_measure(true_measure),
        _convert_to_measure(false_measure) if false_measure is not None else None,
        measure_conditions,
    )


def conjunction(*measures: BooleanMeasure) -> BooleanMeasure:
    """Return a measure equal to the logical conjunction of the passed measures."""
    return BooleanMeasure("and", measures)


def rank(
    measure: Measure,
    hierarchy: Hierarchy,
    ascending: bool = True,
    apply_filters: bool = True,
) -> Measure:
    """Return a measure equal to the rank of a hierarchy's members according to a reference measure.

    Members with equal values are further ranked using the level comparator.

    Example::

        m2 = atoti.rank(m1, hierarchy["date"])

    +------+-------+-----+----+----+------------------------------------------------------+
    | Year | Month | Day | m1 | m2 |                        Comments                      |
    +======+=======+=====+====+====+======================================================+
    | 2000 |       |     | 90 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   01  |     | 25 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  01 | 15 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  02 | 10 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   02  |     | 50 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  01 | 30 |  1 | same value as 2000/02/05 but this member comes first |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  03 | 20 |  3 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 | 30 |  2 |  same value as 2000/02/01 but this member comes last |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   04  |     | 15 |  3 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 |  5 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 | 10 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+

    Args:
        measure: The measure on which the ranking is done.
        hierarchy: The hierarchy containing the members to rank.
        ascending: When set to ``False``, the 1st place goes to the member with greatest value.
        apply_filters: When ``True``, query filters will be applied before ranking members.
            When ``False``, query filters will be applied after the ranking, resulting in "holes" in the ranks.
    """
    return GenericMeasure("RANK", measure, hierarchy, ascending, apply_filters)
