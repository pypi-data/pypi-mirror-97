from __future__ import annotations

import datetime
from typing import Union

from typing_extensions import Literal

from .._measures.calculated_measure import CalculatedMeasure, Operator
from ..measure import Measure, MeasureConvertible, _convert_to_measure

DateOrMeasure = Union[Measure, MeasureConvertible, datetime.date, datetime.datetime]

_Unit = Literal[  # pylint: disable=invalid-name
    "seconds", "minutes", "hours", "days", "weeks", "months", "years"
]


def date_diff(
    from_date: DateOrMeasure,
    to_date: DateOrMeasure,
    *,
    unit: _Unit = "days",
) -> Measure:
    """Return a measure equal to the difference between two dates.

    If one of the date is ``N/A`` then ``None`` is returned.

    Args:
        from_date: The first date measure or object.
        to_date: The second date measure or object.
        unit: The difference unit.
            Seconds, minutes and hours are only allowed if the dates contain time information.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["From", "To"],
        ...     data=[
        ...         ("2020-01-01", "2020-01-02"),
        ...         ("2020-02-01", "2020-02-21"),
        ...         ("2020-03-20", None),
        ...         ("2020-05-15", "2020-04-15"),
        ...     ],
        ... )
        >>> store = session.read_pandas(
        ...     df,
        ...     store_name="date_diff example",
        ...     types={
        ...         "From": tt.type.LOCAL_DATE,
        ...         "To": tt.type.local_date("yyyy-MM-dd", nullable=True),
        ...     },
        ... )
        >>> cube = session.create_cube(store)
        >>> lvl, m = cube.levels, cube.measures
        >>> m["Diff"] = tt.date_diff(lvl["From"], lvl["To"])
        >>> cube.query(
        ...     m["Diff"], m["contributors.COUNT"], levels=[lvl["From"], lvl["To"]]
        ... )
                              Diff contributors.COUNT
        From       To
        2020-01-01 2020-01-02    1                  1
        2020-02-01 2020-02-21   20                  1
        2020-03-20 N/A                              1
        2020-05-15 2020-04-15  -30                  1

    """
    return CalculatedMeasure(
        Operator(
            "datediff",
            [_convert_to_measure(from_date), _convert_to_measure(to_date), unit],
        )
    )
