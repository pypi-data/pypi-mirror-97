from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Collection, Mapping, Optional, Sequence

import numpy as np
import pandas as pd
from typing_extensions import Literal

from ._docs_utils import (
    CSV_KWARGS,
    PARQUET_KWARGS,
    STORE_CREATION_KWARGS,
    STORE_SHARED_KWARGS,
    doc,
)
from ._file_utils import _split_csv_path_and_pattern
from ._local_session import LocalSession
from ._pandas_utils import get_csv_sep_for_pandas_read_load, pandas_to_temporary_csv
from ._path_utils import PathLike, stem_path
from ._plugins import MissingPluginError
from ._sources.csv import CsvDataSource
from ._sources.parquet import ParquetDataSource
from ._type_utils import BASE_SCENARIO, ScenarioName, typecheck
from .config import SessionConfiguration
from .cube import Cube
from .cubes import Cubes
from .exceptions import AtotiException
from .sampling import SamplingMode
from .store import Store, _create_store
from .stores import Stores
from .type import DataType

if TYPE_CHECKING:
    # PySpark is only imported for type checking as we don't want it as a dependency
    from pyspark.sql import DataFrame as SparkDataFrame

_CubeCreationMode = Literal[  # pylint: disable=invalid-name
    "auto", "manual", "no_measures"
]


def _resolve_metadata_db(metadata_db: str) -> str:
    if metadata_db.startswith("jdbc"):
        raise NotImplementedError("jdbc URLs are not yet supported.")

    # Remote URL don't need to be resolved
    if metadata_db.startswith("http://") or metadata_db.startswith("https://"):
        return metadata_db

    # Make sure the parent directory exists.
    path = Path(metadata_db)
    if path.exists() and not path.is_dir():
        raise ValueError(f"metadata_db is not a directory: {metadata_db}")
    path.mkdir(exist_ok=True)

    # Return the fully resolved path.
    return str(path.resolve())


def _find_corresponding_top_level_variable_name(value: Any) -> Optional[str]:
    from IPython import get_ipython

    top_level_variables: Mapping[str, Any] = get_ipython().user_ns

    for variable_name, variable_value in top_level_variables.items():
        is_regular_variable = not variable_name.startswith("_")
        if is_regular_variable and variable_value is value:
            return variable_name

    return None


def _infer_store_name(path: PathLike, store_name: Optional[str]) -> str:
    """Infer the name of a store given the path and store_name parameters."""
    return store_name or stem_path(path).capitalize()


class Session(LocalSession[Cubes]):
    """Holds a connection to the Java gateway."""

    def __init__(
        self,
        name: str,
        *,
        config: SessionConfiguration,
        **kwargs: Any,
    ):
        """Create the session and the Java gateway.

        Args:
            name: The name of the session.
            config: The configuration of the session.

        """
        super().__init__(name, config, False, **kwargs)
        self._cubes = Cubes(self)

        if not config.sampling_mode:
            raise AtotiException("The default sampling mode should have been applied")

        self._sampling_mode = config.sampling_mode

    def __enter__(self) -> Session:
        """Enter this session's context manager.

        Returns:
            self: to assign it to the "as" keyword.

        """
        return self

    @property
    def cubes(self) -> Cubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def stores(self) -> Stores:  # noqa: D401
        """Stores of the session."""
        return Stores(
            self._java_api,
            {
                store: Store(store, self._java_api)
                for store in self._java_api.get_stores()
            },
        )

    @doc(**STORE_CREATION_KWARGS)
    def create_store(
        self,
        types: Mapping[str, DataType],
        store_name: str,
        *,
        keys: Optional[Collection[str]] = None,
        partitioning: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
        hierarchized_columns: Optional[Collection[str]] = None,
    ) -> Store:
        """Create a store from a schema.

        Args:
            types: Types for all columns of the store.
                This defines the columns which will be expected in any future data loaded into the store.
            {store_name}
            {keys}
            {partitioning}
            {sampling_mode}
            {hierarchized_columns}

        """
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode
        self._java_api.create_store(
            types, store_name, keys, partitioning, mode, hierarchized_columns
        )
        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    def read_pandas(
        self,
        dataframe: pd.DataFrame,  # type: ignore
        store_name: str,
        *,
        keys: Optional[Collection[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        types: Optional[Mapping[str, DataType]] = None,
        hierarchized_columns: Optional[Collection[str]] = None,
        **kwargs: Any,
    ) -> Store:
        """Read a pandas DataFrame into a store.

        All the named indices of the DataFrame are included into the store.
        Multilevel columns are flattened into a single string name.

        Args:
            dataframe: The DataFrame to load.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}
            types: Types for some or all columns of the store.
                Types for non specified columns will be inferred.
            {hierarchized_columns}

        Returns:
            The created store holding the content of the DataFrame.
        """
        # set sep to | because can contains list with sep , [x, y, ...]
        sep, kwargs = get_csv_sep_for_pandas_read_load(kwargs)
        file_path, atoti_types_mapping = pandas_to_temporary_csv(
            dataframe, sep, prefix=store_name
        )
        # Set the inferred type of key fields to non nullable
        clean_atoti_types_mapping = {
            name: DataType(field_type.java_type, False)
            if field_type.nullable and keys is not None and name in keys
            else field_type
            for (name, field_type) in atoti_types_mapping.items()
        }
        if types is not None:
            clean_atoti_types_mapping = {
                **clean_atoti_types_mapping,
                **types,
            }
        return self.read_csv(
            file_path,
            keys=keys,
            in_all_scenarios=in_all_scenarios,
            store_name=store_name,
            partitioning=partitioning,
            types=clean_atoti_types_mapping,
            sep=sep,
            hierarchized_columns=hierarchized_columns,
            **kwargs,
        )

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    @typecheck(ignored_params=["dataframe"])
    def read_spark(
        self,
        dataframe: SparkDataFrame,  # type: ignore
        store_name: str,
        *,
        keys: Optional[Collection[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        hierarchized_columns: Optional[Collection[str]] = None,
    ) -> Store:
        """Read a Spark DataFrame into a store.

        Args:
            dataframe: The DataFrame to load.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}
            {hierarchized_columns}

        Returns:
            The created store holding the content of the DataFrame.
        """
        from ._spark_utils import spark_to_temporary_parquet

        # Create a Parquet and read it
        file_name = spark_to_temporary_parquet(dataframe, store_name)
        return self.read_parquet(
            path=file_name,
            keys=keys,
            store_name=store_name,
            in_all_scenarios=in_all_scenarios,
            partitioning=partitioning,
            hierarchized_columns=hierarchized_columns,
        )

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS, **CSV_KWARGS})
    def read_csv(
        self,
        path: PathLike,
        *,
        keys: Optional[Collection[str]] = None,
        store_name: Optional[str] = None,
        in_all_scenarios: bool = True,
        sep: Optional[str] = None,
        encoding: str = "utf-8",
        process_quotes: Optional[bool] = None,
        partitioning: Optional[str] = None,
        types: Optional[Mapping[str, DataType]] = None,
        watch: bool = False,
        array_sep: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
        hierarchized_columns: Optional[Collection[str]] = None,
    ) -> Store:
        """Read a CSV file into a store.

        Args:
            {path}
            {keys}
            store_name: The name of the store to create.
                Defaults to the final component of the given ``path``.
            {in_all_scenarios}
            {sep}
            {encoding}
            {process_quotes}
            {partitioning}
            types: Types for some or all columns of the store.
                Types for non specified columns will be inferred from the first 1,000 lines.
            {watch}
            {array_sep}
            {sampling_mode}
            {hierarchized_columns}

        Returns:
            The created store holding the content of the CSV file(s).
        """
        path, pattern = _split_csv_path_and_pattern(path)

        store_name = _infer_store_name(path, store_name)

        # Load the CSV into the store
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode
        CsvDataSource(self._java_api).create_store_from_csv(
            path,
            store_name,
            keys,
            in_all_scenarios,
            sep,
            encoding,
            process_quotes,
            partitioning,
            types,
            watch,
            array_sep,
            pattern,
            mode,
            hierarchized_columns,
        )

        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS, **PARQUET_KWARGS})
    def read_parquet(
        self,
        path: PathLike,
        *,
        keys: Optional[Collection[str]] = None,
        store_name: Optional[str] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
        watch: bool = False,
        hierarchized_columns: Optional[Collection[str]] = None,
    ) -> Store:
        """Read a Parquet file into a store.

        Args:
            {path}
            {keys}
            store_name: The name of the store to create.
                Defaults to the final component of the given ``path``.
            {in_all_scenarios}
            {partitioning}
            {sampling_mode}
            {watch}
            {hierarchized_columns}

        Returns:
            The created store holding the content of the Parquet file(s).
        """
        store_name = _infer_store_name(path, store_name)
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode
        # Load the parquet into the store
        ParquetDataSource(self._java_api).create_store_from_parquet(
            path,
            store_name,
            keys,
            in_all_scenarios,
            partitioning,
            mode,
            watch,
            hierarchized_columns,
        )
        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    def read_numpy(
        self,
        array: np.ndarray,  # type: ignore
        columns: Sequence[str],
        store_name: str,
        *,
        keys: Optional[Collection[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        hierarchized_columns: Optional[Collection[str]] = None,
        **kwargs: Any,
    ) -> Store:
        """Read a NumPy 2D array into a new store.

        Args:
            array: The NumPy 2D ndarray to read the data from.
            columns: The names to use for the store's columns.
                They must be in the same order as the values in the NumPy array.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}
            {hierarchized_columns}

        Returns:
            The created store holding the content of the array.
        """
        from ._numpy_utils import numpy_to_temporary_csv

        # We start by checking the provided parameters are of the correct dimension:
        if not len(array.shape) == 2:
            raise AssertionError("Provided array must be 2 dimensional")
        if not len(columns) == array.shape[1]:
            raise AssertionError(
                "Length of columns must be the same as the length of the provided rows"
            )
        sep = kwargs.get("sep", "|")
        path = numpy_to_temporary_csv(array, columns, sep, prefix=store_name)
        return self.read_csv(
            path,
            store_name=store_name,
            sep="|",
            keys=keys,
            in_all_scenarios=in_all_scenarios,
            partitioning=partitioning,
            hierarchized_columns=hierarchized_columns,
        )

    def read_sql(  # pylint: disable=no-self-use
        self, *args: Any, **kwargs: Any
    ) -> Store:
        """atoti-sql is required."""
        raise MissingPluginError("sql")

    def create_cube(
        self,
        base_store: Store,
        name: Optional[str] = None,
        *,
        mode: _CubeCreationMode = "auto",
    ) -> Cube:
        """Create a cube using based on the passed store.

        Args:
            base_store: The cube's base store.
            name: The name of the created cube.
                Defaults to the name of the base store.
            mode: The cube creation mode:

                * ``auto``: Creates hierarchies for every non-numeric column, and measures for every numeric column.
                * ``manual``: Does not create any hierarchy or measure (except from the count).
                * ``no_measures``: Creates the hierarchies like ``auto`` but does not create any measures.

                For stores with ``hierarchized_columns`` specified, these will be converted into
                hierarchies regardless of the cube creation mode.

        See Also:
            Hierarchies and measures created by a :meth:`~atoti.store.Store.join`.
        """
        if name is None:
            name = base_store.name

        self._java_api.create_cube_from_store(base_store, name, mode.upper())
        self._java_api.refresh(force_start=True)
        Cube(self._java_api, name, base_store, self)

        return self.cubes[name]

    def create_scenario(self, name: str, *, origin: str = BASE_SCENARIO):
        """Create a new source scenario in the datastore.

        Args:
            name: The name of the scenario.
            origin: The scenario to fork.
        """
        self._java_api.create_scenario(ScenarioName(name), ScenarioName(origin))

    def load_all_data(self):
        """Trigger the :data:`full <atoti.sampling.FULL>` loading of the data.

        Calling this method will change the :mod:`sampling mode <atoti.sampling>` to :data:`atoti.sampling.FULL` which triggers the loading of all the data.
        All subsequent loads, including new stores, will not be sampled.

        When building a project, this method should be called as late as possible.
        """
        self._java_api.load_all_data()
        self._java_api.refresh()

    def delete_scenario(self, scenario: str) -> None:
        """Delete the source scenario with the provided name if it exists."""
        _scenario = ScenarioName(scenario)
        if _scenario == BASE_SCENARIO:
            raise ValueError("Cannot delete the base scenario")
        self._java_api.delete_scenario(_scenario)

    @property
    def scenarios(self) -> Collection[str]:  # noqa: D401
        """Collection of source scenarios of the session."""
        return self._java_api.get_scenarios()

    def export_translations_template(self, path: PathLike):
        """Export a template containing all translatable values in the session's cubes.

        Args:
            path: The path at which to write the template.
        """
        self._java_api.export_i18n_template(path)
