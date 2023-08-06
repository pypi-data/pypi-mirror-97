from typing import Optional, Tuple, Union

from atoti.hierarchy import Hierarchy
from atoti.level import Level

from ._utils import CumulativeTimeWindow, CumulativeWindow, LeafLevels, SiblingsWindow
from .scope import Scope


def cumulative(
    level: Level,
    *,
    dense: bool = False,
    partitioning: Optional[Level] = None,
    window: Optional[Union[range, Tuple[Optional[str], Optional[str]]]] = None,
) -> Scope:
    """Create a scope to be used in the computation of cumulative aggregations.

    Cumulative aggregations include cumulative sums (also called running sum or prefix sum), mean, min, max, etc.

    Example::

        m2 = atoti.agg.sum(m1, scope=atoti.scope.cumulative(date))

    +------------+----+----+
    |    date    | m1 | m2 |
    +============+====+====+
    | 2000/01/01 | 15 | 15 |
    +------------+----+----+
    | 2000/01/02 | 10 | 25 |
    +------------+----+----+
    | 2000/02/03 | 20 | 45 |
    +------------+----+----+
    | 2000/02/05 | 30 | 75 |
    +------------+----+----+
    | 2000/04/05 | 5  | 90 |
    +------------+----+----+
    | 2000/04/05 | 10 | 95 |
    +------------+----+----+

    If the level is part of a multi-level hierarchy, it is possible to reset the aggregation when the value of a level changes.
    For instance, a running sum over a date can be reset at the beginning of each month::

        m2 = atoti.agg.sum(m1, scope=atoti.scope.cumulative("day", partitioning="month"))

    +----------------+----+----+------------------------------------+
    | year/month/day | m1 | m2 |              Comment               |
    +================+====+====+====================================+
    |   2000/01/01   | 15 | 15 |                                    |
    +----------------+----+----+------------------------------------+
    |   2000/01/02   | 10 | 25 |                                    |
    +----------------+----+----+------------------------------------+
    |   2000/02/03   | 20 | 20 | Reset at the beginning of February |
    +----------------+----+----+------------------------------------+
    |   2000/02/05   | 30 | 50 |                                    |
    +----------------+----+----+------------------------------------+
    |   2000/04/05   | 5  | 5  | Reset at the beginning of April    |
    +----------------+----+----+------------------------------------+
    |   2000/04/05   | 10 | 15 |                                    |
    +----------------+----+----+------------------------------------+

    Args:
        level: The level along which the aggregation is performed.
        dense: When ``True``, all members of the level, even those with no value for the underlying measure, will be taken into account for the cumulative aggregation (resulting in repeating values).
        partitioning: The levels in the hierarchy at which to start the aggregation over.
        window: The custom aggregation window.
            The window defines the set of members before and after a given member (using the level comparator) to be considered in the computation of the cumulative aggregation.

            The window can be a:

            * ``range`` starting with a <=0 value and ending with a >=0 value.

               By default the window is ``range(-∞, 0)``, meaning that the value for a given member is computed using all of the members before it and none after it.
            * time period as a two-element tuple starting with an offset of the form ``-xxDxxWxxMxxQxxY`` or ``None`` and ending with an offset of the form ``xxDxxWxxMxxQxxY`` or ``None``.

              For instance, to compute the 5 previous days sliding mean::

                m2 = atoti.agg.mean(m1, scope=tt.scope.cumulative("date", window=("-5D", None)))

    """
    if window is not None and isinstance(window, Tuple):
        back = window[0]
        if back is not None and not back.startswith("-"):
            raise ValueError("back period parameter must be a negative time frame.")
        forward = window[1]
        if forward is not None and forward.startswith("-"):
            raise ValueError("forward period parameter must be a positive time frame")
        return CumulativeTimeWindow(level, window, partitioning)

    if window is not None and isinstance(window, range):
        if window.step != 1:
            raise ValueError(
                "Running aggregation windows only support ranges with step of size 1."
            )
        if window.start > 0 or window.stop < 0:
            raise ValueError(
                "Running aggregation window should have a start value less than or equal to 0, "
                "and a stop value greater than or equal to 0."
            )

    return CumulativeWindow(level, dense, window, partitioning)


def siblings(hierarchy: Hierarchy, *, exclude_self: bool = False) -> Scope:
    """Create a "siblings" aggregation scope.

    In a siblings scope, the value for the member of a given level in the hierarchy is computed by taking the contribution of all of the members on the same level (its siblings).

    A siblings aggregation is an appropriate tool for operations such as marginal aggregations (marginal VaR, marginal mean) for non-linear aggregation functions.

    Args:
        hierarchy: The hierarchy containing the levels along which the aggregation is performed.
        exclude_self: Whether to include the current member's contribution in its cumulative value.
    """
    return SiblingsWindow(
        hierarchy,
        exclude_self,
    )


def origin(*levels: Level) -> Scope:
    """Create an aggregation scope with an arbitrary number of levels.

    The passed levels define a boundary above and under which the aggregation is performed differently.
    When those levels are not expressed in a query, the measure will drill down until finding the value for all members of these levels, and then aggregate those values using the user-defined aggregation function.
    This allows to compute measures that show the yearly mean when looking at the grand total, but the sum of each month's value when looking at each year individually.

    Args:
        levels: The levels defining the dynamic aggregation domain.
    """
    if len(levels) == 1 and isinstance(levels[0], list):
        raise TypeError("origin takes one or more levels, not a list.")

    return LeafLevels(list(levels))
