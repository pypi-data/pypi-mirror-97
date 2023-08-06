from typing import Mapping

from ..column import Column
from ..cube import Cube


def create_date_hierarchy(  # pylint: disable=dangerous-default-value
    name: str,
    cube: Cube,
    column: Column,
    *,
    levels: Mapping[str, str] = {"Year": "Y", "Month": "M", "Day": "d"},
):
    """Create a multilevel date hierarchy based on a date column.

    The new levels are created by matching a date pattern.
    Here is a non-exhaustive list of patterns that can be used:

        +---------+-----------------------------+---------+-----------------------------------+
        | Pattern | Description                 | Type    | Examples                          |
        +=========+=============================+=========+===================================+
        | Y       | Year                        | Integer | ``2001, 2005, 2020``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | YY      | 2-digits year               | String  | ``"01", "05", "20"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | YYYY    | 4-digits year               | String  | ``"2001", "2005", "2020"``        |
        +---------+-----------------------------+---------+-----------------------------------+
        | M       | Month of the year (1 based) | Integer | ``1, 5, 12``                      |
        +---------+-----------------------------+---------+-----------------------------------+
        | MM      | 2-digits month              | String  | ``"01", "05", "12"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | MMM     | 3-letters month             | String  | ``"Jan", "May", "Dec"``           |
        +---------+-----------------------------+---------+-----------------------------------+
        | MMMM    | Full month                  | String  | ``"January", "May", "December"``  |
        +---------+-----------------------------+---------+-----------------------------------+
        | d       | Day of the month            | Integer | ``1, 15, 30``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | dd      | 2-digits day of the month   | String  | ``"01", "15", "30"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | w       | Week number                 | Integer | ``1, 12, 51``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | eeee    | Day of the week             | String  | ``"Monday", "Tuesday", "Sunday"`` |
        +---------+-----------------------------+---------+-----------------------------------+
        | Q       | Quarter                     | Integer | ``1, 2, 3, 4``                    |
        +---------+-----------------------------+---------+-----------------------------------+
        | QQQ     | Quarter prefixed with Q     | String  | ``"Q1", "Q2", "Q3", "Q4"``        |
        +---------+-----------------------------+---------+-----------------------------------+
        | H       | Hour of day (0-23)          | Integer | ``0, 12, 23``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | HH      | 2-digits hour of day        | String  | ``"00", "12", "23"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | m       | Minute of hour              | Integer | ``0, 30, 59``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | mm      | 2-digits minute of hour     | String  | ``"00", "30", "59"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | s       | Second of minute            | Integer | ``0, 5, 55``                      |
        +---------+-----------------------------+---------+-----------------------------------+
        | ss      | 2-digits second of minute   | String  | ``"00", "05", "55"``              |
        +---------+-----------------------------+---------+-----------------------------------+

    Supported patterns are the ones of the `DateTimeFormatter in Java <https://docs.oracle.com/en/java/javase/15/docs/api/java.base/java/time/format/DateTimeFormatter.html>`_.

    Args:
        name: The name of the hierarchy to create.
        cube: The cube of the new hierarchy.
        column: A store column containing a date or a datetime.
        levels: The mapping from the names of the levels to the patterns from which they will be created.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Date", "Quantity"],
        ...     data=[
        ...         ("2020-01-10", 150.0),
        ...         ("2020-01-20", 240.0),
        ...         ("2019-03-17", 270.0),
        ...         ("2019-12-12", 200.0),
        ...     ],
        ... )
        >>> store = session.read_pandas(
        ...     df, keys=["Date"], store_name="create_date_hierarchy example"
        ... )
        >>> cube = session.create_cube(store)
        >>> lvl, m = cube.levels, cube.measures
        >>> tt.experimental.create_date_hierarchy(
        ...     "Date parts",
        ...     cube,
        ...     store["Date"],
        ...     levels={"Year": "Y", "Month": "MMMM", "Day": "d"},
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     include_totals=True,
        ...     levels=[lvl["Year"], lvl["Month"], lvl["Day"]],
        ... )
                           Quantity.SUM
        Year  Month    Day
        Total                    860.00
        2019                     470.00
              December           200.00
                       12        200.00
              March              270.00
                       17        270.00
        2020                     390.00
              January            390.00
                       10        150.00
                       20        240.00

        The full date can also be added back as the last level of the hierarchy:

        >>> h = cube.hierarchies
        >>> h["Date parts"] = {**h["Date parts"].levels, "Date": store["Date"]}
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     include_totals=True,
        ...     levels=lvl["Date parts", "Date"],
        ... )
                                      Quantity.SUM
        Year  Month    Day Date
        Total                               860.00
        2019                                470.00
              December                      200.00
                       12                   200.00
                           2019-12-12       200.00
              March                         270.00
                       17                   270.00
                           2019-03-17       270.00
        2020                                390.00
              January                       390.00
                       10                   150.00
                           2020-01-10       150.00
                       20                   240.00
                           2020-01-20       240.00

    """
    # The dangerous default levels dictionary must not be modified.
    # pylint: disable=protected-access
    cube._java_api.create_date_hierarchy(
        cube,
        column._store,
        column.name,
        name,
        {**levels},
    )
    cube._java_api.refresh()
    # pylint: enable=protected-access
