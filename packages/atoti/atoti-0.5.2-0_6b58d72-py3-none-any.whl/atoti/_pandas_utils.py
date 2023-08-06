import logging
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple, Type

import numpy as np
import pandas as pd

from ._file_utils import _make_atoti_tempir
from .type import NULLABLE_DOUBLE, NULLABLE_FLOAT, NULLABLE_INT, NULLABLE_LONG, DataType

COLUMN_LEVEL_SEPARTOR = "_"


# no type stubs for pandas, so we ignore this error
def pandas_to_temporary_csv(
    dataframe: pd.DataFrame,  # type: ignore
    sep: str,
    *,
    prefix: Optional[str] = None,
) -> Tuple[Path, Mapping[str, DataType]]:
    """Convert a pandas DataFrame to a temporary CSV file in a temporary folder.

    All the named indices of the DataFrame are included into the CSV.

    Args:
        dataframe: the DataFrame to convert.
        sep: The separator to use when wirtting the csv.
        prefix: The prefix to give to the randomly generated filename.

    Returns:
        A tuple containing:
        * The path to the temporary file.
        * A mapping from the DataFrame's column names to their inferred atoti type.
          The mapping will only contain the columns for which a matching type has been inferred.

    """
    tempdir: str = _make_atoti_tempir()
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        dir=tempdir,
        suffix=".pdcvs",
        encoding="utf8",
        prefix=prefix,
    ) as file_path:
        # Clean the dataframe.
        clean_dataframe = _clean_index(dataframe)
        _flatten_dataframe(clean_dataframe)

        # Dump it into a CSV file.
        clean_dataframe.to_csv(file_path, index=False, line_terminator="\n", sep=sep)

        # Return the file path and types mapping.
        return (Path(file_path.name), atoti_types_mapping(clean_dataframe))


def _flatten_dataframe(dataframe: pd.DataFrame):  # type: ignore
    """Flatten the columns of the dataframe if they are multilevel."""
    new_columns = []
    for col in dataframe.columns.to_flat_index():
        if isinstance(col, tuple):
            # If the column is multilevel we remove null elements and join the others
            # pandas uses math.nan when a level is not defined
            col = (lvl for lvl in col if not pd.isnull(lvl))
            new_columns.append(COLUMN_LEVEL_SEPARTOR.join(map(str, col)))
        else:
            new_columns.append(col)
    dataframe.columns = pd.Index(new_columns)


def _clean_index(data: pd.DataFrame) -> pd.DataFrame:  # type: ignore
    """Un-index the dataframe.

    The named indices are moved to regular columns and the unnamed ones are dropped.
    """
    # Remove the valid columns from the index and keep them.
    dataframe = data.reset_index(
        level=[col for col in data.index.names if col is not None], drop=False
    )

    # Get rid of the remaining (unnamed) ones and return.
    dataframe = dataframe.reset_index(drop=True)

    if dataframe is None:
        raise TypeError("expected dataframe to be defined")

    return dataframe


def atoti_types_mapping(dataframe: pd.DataFrame) -> Mapping[str, DataType]:  # type: ignore
    """Compute the atoti type of each column in the DataFrame.

    The index columns are ignored.

    Args:
        dataframe: a pandas DataFrame.

    Returns:
        A mapping from the column names to their associated atoti type.
        The mapping will only contain the columns for which a matching type has been inferred.
    """
    # Transform the pandas data types into atoti's data types for each column in the dataframe.
    columns_atoti_types = {
        column_name: np_to_atoti_type(dtype.type)
        for (column_name, dtype) in dataframe.dtypes.iteritems()
    }

    # Only keep the columns for which the atoti's type has been inferred.
    return {
        column_name: atoti_type
        for (column_name, atoti_type) in columns_atoti_types.items()
        if atoti_type is not None
    }


def np_to_atoti_type(type_cls: Type[Any]) -> Optional[DataType]:
    """Compute the atoti type associated with the input type class.

    Args:
        type_cls: A type class. Typically a subclass of np.generic or a built-in Python type.

    Returns:
        The associated atoti type, or None if no matching type has been found.
    """
    # See :
    #   https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dtypes
    #   https://numpy.org/devdocs/reference/arrays.scalars.html

    # Integer types
    if issubclass(type_cls, np.integer):
        return NULLABLE_INT if np.nbytes[type_cls] <= 4 else NULLABLE_LONG
    if issubclass(type_cls, int):
        return NULLABLE_LONG

    # Floating types
    if issubclass(type_cls, np.floating):
        return NULLABLE_FLOAT if np.nbytes[type_cls] <= 4 else NULLABLE_DOUBLE
    if issubclass(type_cls, float):
        return NULLABLE_DOUBLE

    # pandas date type (np.datetime64) seems to represent both date and datetime
    # and I could not find a way to discriminate them.
    # We don't handle them specifically, we should be OK because atoti's CSV
    # discovery should be able to correctly detect date formats.

    # Cannot guess.
    return None


def get_csv_sep_for_pandas_read_load(
    kwargs: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    """Get seperator for CSv an display a wrning if the user specify one.

    User shouldn't specify a sep because its DataFrame can contain Python list with ``,``.

    Args:
        kwargs: kwargs of the method read_pandas or load_pandas.

    Returns:
        The sep, by default ``|`` if not specified in kwargs and the cleaned kwargs.
    """
    sep = "|"
    if "sep" in kwargs:
        sep = kwargs.pop("sep")
        if sep == ",":
            logging.getLogger(  # pylint: disable=logging-not-lazy
                "atoti.session"
            ).warning(
                "Argument sep=',' can be used in read_pandas or load_pandas only"
                + "if your dataframe does not contains python List"
            )
    return sep, kwargs
