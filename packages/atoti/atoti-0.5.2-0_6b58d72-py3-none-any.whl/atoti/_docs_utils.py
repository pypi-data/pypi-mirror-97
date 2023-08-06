from functools import wraps
from textwrap import dedent
from typing import Any, Callable, List, Union, cast

from ._type_utils import F


# Taken from Pandas:
# https://github.com/pandas-dev/pandas/blame/8aa707298428801199280b2b994632080591700a/pandas/util/_decorators.py#L332
def doc(*args: Union[str, Callable[..., Any]], **kwargs: str) -> Callable[[F], F]:
    """Take docstring templates, concatenate them and perform string substitution."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            return func(*args, **kwargs)

        # Collecting docstring and docstring templates
        docstring_components: List[Union[str, Callable]] = []
        if func.__doc__:
            docstring_components.append(dedent(func.__doc__))

        for arg in cast(Any, args):
            if hasattr(arg, "_docstring_components"):
                docstring_components.extend(
                    cast(  # pylint: disable=protected-access
                        Any,
                        arg,
                    )._docstring_components
                )
            elif isinstance(arg, str) or arg.__doc__:
                docstring_components.append(arg)

        # Formatting templates and concatenating docstring
        wrapper.__doc__ = "".join(
            [
                arg.format(**kwargs)
                if isinstance(arg, str)
                else dedent(arg.__doc__ or "")
                for arg in docstring_components
            ]
        )

        wrapper._docstring_components = (  # pylint: disable=protected-access
            docstring_components
        )

        return cast(F, wrapper)

    return decorator


STORE_SHARED_KWARGS = {
    "in_all_scenarios": """in_all_scenarios: Whether to load the data in all existing scenarios.""",
    "truncate": "truncate: Whether to clear the store before loading the new data into it.",
    "watch": """watch: Whether the source file or directory at the given ``path`` should be watched for changes.
                When set to ``True``, changes to the source will automatically be reflected in the store.
                If the source is a directory, new files will be loaded into the same store as the initial data and must therefore have the same schema as the initial data as well.""",
}


CSV_KWARGS = {
    "array_sep": """array_sep: The delimiter to use for arrays.
                Setting it to a non-``None`` value will parse all the columns containing this separator as arrays.""",
    "encoding": """encoding: The encoding to use to read the CSV.""",
    "path": """path: The path to the CSV file or directory to load.

                If a path pointing to a directory is provided, all of the files with the ``.csv`` extension in the directory and subdirectories will be loaded into the same store and, as such, they are all expected to share the same schema.

                ``.gz``, ``.tar.gz`` and ``.zip`` files containing compressed CSV(s) are also supported.

                The path can contain glob parameters (e.g. ``path/to/directory/**.*.csv``) and will be expanded correctly.
                Be careful, when using glob expressions in paths, all files which match the expression will be loaded, regardless of their extension.
                When the provided path is a directory, the default glob parameter of ``**.csv`` is used.""",
    "process_quotes": """process_quotes: Whether double quotes should be processed to follow the official CSV specification:

                * ``True``:

                    * Each field may or may not be enclosed in double quotes (however some programs, such as Microsoft Excel, do not use double quotes at all).
                      If fields are not enclosed with double quotes, then double quotes may not appear inside the fields.
                    * A double quote appearing inside a field must be escaped by preceding it with another double quote.
                    * Fields containing line breaks, double quotes, and commas should be enclosed in double-quotes.
                * ``False``: all double-quotes within a field will be treated as any regular character, following Excel's behavior.
                  In this mode, it is expected that fields are not enclosed in double quotes.
                  It is also not possible to have a line break inside a field.
                * ``None``: The behavior will be inferred from the first lines of the CSV file.""",
    "sep": """sep: The delimiter to use.
                If ``None``, the separator will automatically be detected.""",
    "watch": f"""{STORE_SHARED_KWARGS["watch"]}
                Any non-CSV files added to the directory will be ignored.""",
}

HEAD_DOC = """Return ``n`` rows of the {what} as a pandas DataFrame."""

LEVEL_ISIN_DOC = """Return a condition to check that the level is on one of the given members.

        ``level.isin(a, b)`` is equivalent to ``(level == a) OR (level == b)``.

        Args:
            members: One or more members on which the level should be.

        Example:
            .. doctest:: Level.isin

                >>> df = pd.DataFrame(
                ...     columns=["City", "Price"],
                ...     data=[
                ...         ("Berlin", 150.0),
                ...         ("London", 240.0),
                ...         ("New York", 270.0),
                ...         ("Paris", 200.0),
                ...     ],
                ... )
                >>> store = session.read_pandas(
                ...     df, keys=["City"], store_name="isin example"
                ... )
                >>> cube = session.create_cube(store)
                >>> lvl, m = cube.levels, cube.measures
                >>> m["Price.SUM in London and Paris"] = tt.filter(
                ...     m["Price.SUM"], lvl["City"].isin("London", "Paris")
                ... )
                >>> cube.query(
                ...     m["Price.SUM"],
                ...     m["Price.SUM in London and Paris"],
                ...     levels=lvl["City"],
                ... )
                         Price.SUM Price.SUM in London and Paris
                City
                Berlin      150.00
                London      240.00                        240.00
                New York    270.00
                Paris       200.00                        200.00

            .. doctest:: Level.isin
                :hide:

                Clear the session to isolate the multiple methods sharing this docstring.
                >>> session._clear()

"""

HIERARCHY_ISIN_DOC = """Return a condition to check that the hierarchy is on one of the given members.

        Considering ``hierarchy_1`` containing ``level_1`` and ``level_2``, ``hierarchy_1.isin((a,), (b, x))`` is equivalent to ``(level_1 == a) OR ((level_1 == b) AND (level_2 == x))``.

        Args:
            members: One or more members expressed as tuples on which the hierarchy should be.
                Each element in a tuple corresponds to a level of the hierarchy, from the shallowest to the deepest.

        Example:
            .. doctest:: Hierarchy.isin

                >>> df = pd.DataFrame(
                ...     columns=["Country", "City", "Price"],
                ...     data=[
                ...         ("Germany", "Berlin", 150.0),
                ...         ("Germany", "Hamburg", 120.0),
                ...         ("United Kingdom", "London", 240.0),
                ...         ("United States", "New York", 270.0),
                ...         ("France", "Paris", 200.0),
                ...     ],
                ... )
                >>> store = session.read_pandas(
                ...     df, keys=["Country", "City"], store_name="isin example"
                ... )
                >>> cube = session.create_cube(store)
                >>> h, lvl, m = cube.hierarchies, cube.levels, cube.measures
                >>> h["Geography"] = [lvl["Country"], lvl["City"]]
                >>> m["Price.SUM in Germany and Paris"] = tt.filter(
                ...     m["Price.SUM"],
                ...     h["Geography"].isin(("Germany",), ("France", "Paris")),
                ... )
                >>> cube.query(
                ...     m["Price.SUM"],
                ...     m["Price.SUM in Germany and Paris"],
                ...     levels=lvl["Geography", "City"],
                ... )
                                        Price.SUM Price.SUM in Germany and Paris
                Country        City
                France         Paris       200.00                         200.00
                Germany        Berlin      150.00                         150.00
                               Hamburg     120.00                         120.00
                United Kingdom London      240.00
                United States  New York    270.00

            .. doctest:: Hierarchy.isin
                :hide:

                Clear the session to isolate the multiple methods sharing this docstring.
                >>> session._clear()
"""

PARQUET_KWARGS = {
    "path": """path: The path to the Parquet file or directory.
                If the path points to a directory, all the files in the directory and subdirectories will be loaded into the store and, as such, are expected to have the same schema as the store and to be Parquet files."""
}

QUANTILE_DOC = """Return a measure equal to the requested quantile {what}.

    Here is how to obtain the same behaviour as `these standard quantile calculation methods <https://en.wikipedia.org/wiki/Quantile#Estimating_quantiles_from_a_sample>`_:

    * R-1: ``mode="centered"`` and ``interpolation="lower"``
    * R-2: ``mode="centered"`` and ``interpolation="midpoint"``
    * R-3: ``mode="simple"`` and ``interpolation="nearest"``
    * R-4: ``mode="simple"`` and ``interpolation="linear"``
    * R-5: ``mode="centered"`` and ``interpolation="linear"``
    * R-6 (similar to Excel's ``PERCENTILE.EXC``): ``mode="exc"`` and ``interpolation="linear"``
    * R-7 (similar to Excel's ``PERCENTILE.INC``): ``mode="inc"`` and ``interpolation="linear"``
    * R-8 and R-9 are not supported

    The formulae given for the calculation of the quantile index assume a 1-based indexing system.

    Args:
        measure: The measure to get the quantile of.
        q: The quantile to take.
            Must be between ``0`` and ``1``.
            For instance, ``0.95`` is the 95th percentile and ``0.5`` is the median.
        mode: The method used to calculate the index of the quantile.
            Available options are, when searching for the ``q`` quantile of a vector ``X``:

            * ``simple``: ``len(X) * q``
            * ``centered``: ``len(X) * q + 0.5``
            * ``exc``: ``(len(X) + 1) * q``
            * ``inc``: ``(len(X) - 1) * q + 1``

        interpolation: If the quantile index is not an integer, the interpolation decides what value is returned.
            The different options are, considering a quantile index ``k`` with ``i < k < j`` for a sorted vector ``X``:

            - ``linear``: ``v = X[i] + (X[j] - X[i]) * (k - i)``
            - ``lowest``: ``v = X[i]``
            - ``highest``: ``v = X[j]``
            - ``nearest``: ``v = X[i]`` or ``v = X[j]`` depending on which of ``i`` or ``j`` is closest to ``k``
            - ``midpoint``: ``v = (X[i] + X[j]) / 2``
"""

QUANTILE_INDEX_DOC = """Return a measure equal to the index of requested quantile {what}.

    Args:
        measure: The measure to get the quantile of.
        q: The quantile to take.
            Must be between ``0`` and ``1``.
            For instance, ``0.95`` is the 95th percentile and ``0.5`` is the median.
        mode: The method used to calculate the index of the quantile.
            Available options are, when searching for the ``q`` quantile of a vector ``X``:

            * ``simple``: ``len(X) * q``
            * ``centered``: ``len(X) * q + 0.5``
            * ``exc``: ``(len(X) + 1) * q``
            * ``inc``: ``(len(X) - 1) * q + 1``

        interpolation: If the quantile index is not an integer, the interpolation decides what value is returned.
            The different options are, considering a quantile index ``k`` with ``i < k < j`` for the original vector ``X``
            and the sorted vector ``Y``:

            - ``lowest``: the index in ``X`` of ``Y[i]``
            - ``highest``: the index in ``X`` of ``Y[j]``
            - ``nearest``: the index in ``X`` of ``Y[i]`` or ``Y[j]`` depending on which of ``i`` or ``j`` is closest to ``k``
"""

STD_DOC_KWARGS = {
    "op": "standard deviation",
    "population_excel": "STDEV.P",
    "population_formula": "\\sqrt{\\frac{\\sum_{i=0}^{n}(X_i - m)^{2}}{n}}",
    "sample_excel": "STDEV.S",
    "sample_formula": "\\sqrt{\\frac{\\sum_{i=0}^{n} (X_i - m)^{2}}{n - 1}}",
}
VAR_DOC_KWARGS = {
    "op": "variance",
    "population_excel": "VAR.P",
    "population_formula": "\\frac{\\sum_{i=0}^{n}(X_i - m)^{2}}{n}",
    "sample_excel": "VAR.S",
    "sample_formula": "\\frac{\\sum_{i=0}^{n} (X_i - m)^{2}}{n - 1}",
}

STD_AND_VAR_DOC = """Return a measure equal to the {op} {what}.

    Args:
        measure: The measure to get the {op} of.
        mode: One of the supported modes:

            * The ``sample`` {op}, similar to Excel's ``{sample_excel}``, is :math:`{sample_formula}` where ``m`` is the sample mean and ``n`` the size of the sample.
              Use this mode if the data represents a sample of the population.
            * The ``population`` {op}, similar to Excel's ``{population_excel}`` is :math:`{population_formula}` where ``m`` is the mean of the ``Xi`` elements and ``n`` the size of the population.
              Use this mode if the data represents the entire population.
"""

STORE_APPEND_DOC = """Add one or multiple rows to the {what}.

        If a row with the same keys already exist in the {what}, it will be overridden by the passed one.

        Args:
            rows: The rows to add.
                Rows can either be:

                * Tuples of values in the correct order.
                * Column name to value mappings.

                All rows must share the shame shape.
            in_all_scenarios: Whether or not the data should be loaded into all of the store's scenarios or only the current one.
"""

SIMULATION_APPEND_DOC = """Add one or multiple rows to the {what}.

        If a row with the same keys already exist in the {what}, it will be overridden by the passed one.

        Args:
            rows: The rows to add.
                Rows can either be:

                * Tuples of values in the correct order.
                * Column name to value mappings.

                All rows must share the shame shape.
"""

STORE_CREATION_KWARGS = {
    "keys": """keys: The columns that will become keys of the store.""",
    "partitioning": """partitioning : The description of how the data will be split across partitions of the store.

                Default rules:

                    * Only non-referenced base stores are automatically partitioned.
                    * Base stores are automatically partitioned by hashing their key fields.
                      If there are no key fields, all the dictionarized fields are hashed.
                    * Referenced stores can only use a sub-partitionning of the store referencing them.
                    * Automatic partitioning is done modulo the number of available processors.

                For instance, ``hash4(country)`` split the data across 4 partitions based on the ``country`` column's hash value.

                Only key columns can be used in the partitioning description.""",
    "sampling_mode": """sampling_mode: The sampling mode. Defaults to this session's one.""",
    "store_name": """store_name: The name of the store to create.""",
    "hierarchized_columns": """hierarchized_columns: The list of columns which will automatically be converted into hierarchies no matter which creation mode is used for the cube.

                The different behaviors based on the passed value are:

                    * ``None``: all non-numeric columns are converted into hierarchies, depending on the cube's creation mode.
                    * Empty collection: no columns are converted into hierarchies.
                    * Non-empty collection: only the columns in the collection will be converted into hierarchies.

                For partial joins, the un-mapped key columns of the target store are always converted into hierarchies, regardless of the value of this parameter.
        """,
}

STORE_IADD_DOC = """Add a single row to the {what}."""
