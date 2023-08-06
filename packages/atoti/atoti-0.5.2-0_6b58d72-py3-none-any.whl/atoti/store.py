from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Sequence, Tuple, Union

import pandas as pd

from ._bitwise_operators_only import IdentityElement
from ._docs_utils import (
    CSV_KWARGS,
    HEAD_DOC,
    PARQUET_KWARGS,
    STORE_APPEND_DOC,
    STORE_IADD_DOC,
    STORE_SHARED_KWARGS,
    doc,
)
from ._file_utils import (
    _split_csv_path_and_pattern,
    _validate_csv_path,
    _validate_glob_pattern,
)
from ._ipython_utils import ipython_key_completions_for_mapping
from ._java_api import JavaApi
from ._pandas_utils import get_csv_sep_for_pandas_read_load
from ._plugins import MissingPluginError
from ._repr_utils import ReprJson, ReprJsonable
from ._sources.csv import CsvDataSource, MultiScenarioCsvDataSource
from ._sources.parquet import ParquetDataSource
from ._spark_utils import spark_to_temporary_parquet
from ._type_utils import BASE_SCENARIO, ScenarioName, typecheck
from .column import Column
from .report import StoreReport
from .sampling import SamplingMode, _get_warning_message
from .type import DataType

if TYPE_CHECKING:
    from pyspark.sql import DataFrame as SparkDataFrame

# Type for store rows
Row = Union[Tuple[Any, ...], Mapping[str, Any]]

_DOC_KWARGS = {"what": "store"}


@dataclass
class Store(ReprJsonable):
    """Represents a single store."""

    _name: str
    _java_api: JavaApi = field(repr=False)
    _scenario: ScenarioName = field(default=BASE_SCENARIO)
    _columns: Dict[str, Column] = field(default_factory=dict)

    def __post_init__(self):
        """Finish initialization."""
        for col in self._java_api.get_store_schema(self):
            data_type = DataType(col.column_type_name, col.is_nullable)
            self._columns[col.name] = Column(col.name, data_type, self)

    @property
    def name(self) -> str:
        """Name of the store."""
        return self._name

    @property
    def keys(self) -> Sequence[str]:
        """Names of the key columns of the stores."""
        return self._java_api.get_key_columns(self)

    @property
    def scenario(self) -> ScenarioName:
        """Scenario on which the store is."""
        return self._scenario

    @property
    def columns(self) -> Sequence[str]:
        """Columns of the stores."""
        return list(self._columns.keys())

    @property
    def _sampling_mode(self) -> SamplingMode:
        """Return the sampling mode of the store."""
        return self._java_api.get_sampling_mode(self)

    @property
    def _types(self) -> Mapping[str, DataType]:
        """Columns and their types."""
        return {name: col.data_type for name, col in self._columns.items()}

    @property
    def _partitioning(self) -> str:
        """Store partitioning."""
        return self._java_api.get_store_partitioning(self)

    def join(
        self,
        other: Store,
        *,
        mapping: Optional[Mapping[str, str]] = None,
    ):
        """Define a reference between this store and another.

        There are two different possible situations when creating references:

        * All the key columns of the ``other`` store are mapped: this is a normal reference.
        * Only some of the key columns of the ``other`` store are mapped: this is a partial reference:

            * The columns from the base store used in the mapping must be attached to hierarchies.
            * The un-mapped key columns of the ``other`` store will be converted into hierarchies.

        Depending on the cube creation mode, the join will also generate different hierarchies and measures:

        * ``manual``: The un-mapped keys of the ``other`` store will become hierarchies.
        * ``no_measures``: All of the non-numeric columns from the ``other`` store, as well as those containing integers, will be converted into hierarchies.
          No measures will be created in this mode.
        * ``auto``: The same hierarchies will be created as in the ``no_measures`` mode.
          Additionally, columns of the base store containing numeric values, or arrays, except for columns which contain only integers, will be converted into measures.
          Columns of the ``other`` store with these types will not be converted into measures.

        Args:
            other: The other store to reference.
            mapping: The column mapping of the reference.
                Defaults to the columns with the same names in the two stores.
        """
        self._java_api.create_join(
            store=self,
            other_store=other,
            mappings=mapping,
        )
        self._java_api.refresh(force_start=False)

    @property
    def source_simulation_enabled(self) -> bool:
        """Whether source simulations are enabled on the store."""
        return self._java_api.get_source_simulation_enabled(self)

    @source_simulation_enabled.setter
    def source_simulation_enabled(self, enabled: bool):
        """Enable or disable the source simulation."""
        self._java_api.set_source_simulation_enabled(self, enabled)

    @property
    def shape(self) -> Mapping[str, int]:
        """Shape of the store."""
        return {"rows": len(self), "columns": len(self._columns)}

    @property
    def scenarios(self) -> StoreScenarios:
        """All the scenarios the store can be on."""
        if self.scenario != BASE_SCENARIO:
            raise Exception("You can only create a new scenario from the base scenario")
        return StoreScenarios(self._java_api, self)

    @property
    def loading_report(self) -> StoreReport:
        """Store loading report."""
        reports = self._java_api.get_loading_report(self)
        return StoreReport(self.name, reports)

    def __getitem__(self, key: str) -> Column:
        """Return the column with the given name."""
        return self._columns[key]

    def __len__(self) -> int:
        """Return the number of rows in the store."""
        return self._java_api.get_store_size(self)

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self._columns)

    def _check_if_sampling_policy_is_respected(self):
        """Check if the sampling policy is respected and warn if necessary."""
        if self._java_api.should_warn_for_store_sampling_policy(self):
            msg = "The store has been sampled because "
            msg += _get_warning_message(
                self._sampling_mode  # pylint: disable=protected-access
            )
            msg += " Call Session.load_all_data()"
            msg += " to trigger the full load of the data."
            logging.getLogger("atoti.loading").warning(msg)

    @doc(STORE_APPEND_DOC, **_DOC_KWARGS)
    def append(self, *rows: Row, in_all_scenarios: bool = False):
        self._java_api.insert_multiple_in_store(
            self, self.scenario, rows, in_all_scenarios
        )

    @doc(STORE_IADD_DOC, **_DOC_KWARGS)
    def __iadd__(self, row: Row) -> Store:
        """Add a single row to the store."""
        self.append(row)
        return self

    def drop(self, *coordinates: Mapping[str, Any], in_all_scenarios: bool = False):
        """Delete rows where the values for each column match those specified.

        Each set of coordinates can only contain one value for each column.
        To specify mulitple values for one column, mulitple mappings must be passed.

        Args:
            coordinates: Mappings between store columns and values.
                Rows which match the provided mappings will be deleted from the store.
            in_all_scenarios: Whether or not the rows should be dropped on all of the store's scenarios or just the current one.
        """
        self._java_api.delete_rows_from_store(
            self, self.scenario, coordinates, in_all_scenarios
        )

    def _repr_json_(self) -> ReprJson:
        key_cols = self.keys
        # pylint: disable=protected-access
        schema = {
            c.name: {
                "key": c.name in key_cols,
                "nullable": c.data_type.nullable,
                "type": c.data_type.java_type,
            }
            for c in list(self._columns.values())
        }
        # pylint: enable=protected-access
        return schema, {"expanded": True, "root": self.name}

    @doc(HEAD_DOC, **_DOC_KWARGS)
    def head(self, n: int = 5) -> pd.DataFrame:
        if n < 1:
            raise ValueError("n must be at least 1.")

        return self._java_api.get_store_dataframe(self, n, self.scenario, self.keys)

    @doc(**{**STORE_SHARED_KWARGS, **CSV_KWARGS})
    def load_csv(
        self,
        path: Union[pathlib.Path, str],
        *,
        sep: Optional[str] = None,
        encoding: str = "utf-8",
        process_quotes: bool = True,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        watch: bool = False,
        array_sep: Optional[str] = None,
    ):
        """Load a CSV into this scenario.

        Args:
            {path}
            {sep}
            {encoding}
            {process_quotes}
            {in_all_scenarios}
            {truncate}
            {watch}
            {array_sep}
        """
        path, pattern = _split_csv_path_and_pattern(path)

        CsvDataSource(self._java_api).load_csv_into_store(
            path,
            self,
            self.scenario,
            in_all_scenarios,
            sep,
            encoding,
            process_quotes,
            truncate,
            watch,
            array_sep,
            pattern,
        )
        self._check_if_sampling_policy_is_respected()

    @doc(**STORE_SHARED_KWARGS)
    def load_pandas(
        self,
        dataframe: pd.DataFrame,  # type: ignore
        *,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        **kwargs: Any,
    ):
        """Load a pandas DataFrame into this scenario.

        Args:
            dataframe: The DataFrame to load.
            {in_all_scenarios}
            {truncate}
        """
        from ._pandas_utils import pandas_to_temporary_csv

        # set sep to | because can contains list with sep , [x, y, ...]
        sep, kwargs = get_csv_sep_for_pandas_read_load(kwargs)

        # Save DataFrame as CSV then read it
        csv_file, _ = pandas_to_temporary_csv(dataframe, sep)
        self.load_csv(
            csv_file,
            in_all_scenarios=in_all_scenarios,
            truncate=truncate,
            sep=sep,
            **kwargs,
        )

    @doc(**{**STORE_SHARED_KWARGS, **PARQUET_KWARGS})
    def load_parquet(
        self,
        path: Union[pathlib.Path, str],
        *,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        watch: bool = False,
    ):
        """Load a Parquet file into this scenario.

        Args:
            {path}
            {in_all_scenarios}
            {truncate}
            {watch}
        """
        ParquetDataSource(self._java_api).load_parquet_into_store(
            path,
            self,
            self.scenario,
            in_all_scenarios=in_all_scenarios,
            truncate=truncate,
            watch=watch,
        )
        self._check_if_sampling_policy_is_respected()

    @doc(**STORE_SHARED_KWARGS)
    @typecheck(ignored_params=["dataframe"])
    def load_spark(
        self,
        dataframe: SparkDataFrame,  # type: ignore
        *,
        in_all_scenarios: bool = False,
        truncate: bool = False,
    ):
        """Load a Spark DataFrame into this scenario.

        Args:
            dataframe: The dataframe to load.
            {in_all_scenarios}
            {truncate}
        """
        parquet_file = spark_to_temporary_parquet(dataframe)
        self.load_parquet(
            parquet_file,
            in_all_scenarios=in_all_scenarios,
            truncate=truncate,
        )

    def load_kafka(self, *args: Any, **kwargs: Any):  # pylint: disable=no-self-use
        """atoti-kafka is required."""
        raise MissingPluginError("kafka")

    def load_sql(self, *args: Any, **kwargs: Any):  # pylint: disable=no-self-use
        """atoti-sql is required."""
        raise MissingPluginError("sql")

    def _identity(self) -> Tuple[IdentityElement, ...]:
        identity = (self._name, self._scenario)
        for name, column in self._columns.items():
            identity += (name,) + column._identity()  # pylint: disable=protected-access
        return identity


def _create_store(java_api: JavaApi, name: str) -> Store:
    """Create a store and refresh the session.

    Args:
        java_api: The Java API.
        name: The name of the store.
    """
    store = Store(name, java_api)
    # Refresh only happens if the cube was already started.
    java_api.refresh(force_start=False)
    store._check_if_sampling_policy_is_respected()  # pylint: disable=protected-access
    return store


@dataclass(frozen=True)
class StoreScenarios:
    """Scenarios of a store."""

    _java_api: JavaApi = field(repr=False)
    _store: Store = field(repr=False)

    def __getitem__(self, key: str) -> Store:
        """Get the scenario or create it if it does not exist.

        Args:
            key: the name of the scenario

        """
        return Store(self._store.name, self._java_api, ScenarioName(key))

    def __delitem__(self, key: str) -> None:
        """Override base del method to throw an error."""
        raise Exception(
            "You cannot delete a scenario from a store since they are shared between all stores."
            "Use the Session.delete_scenario() method instead."
        )

    @doc(**{**STORE_SHARED_KWARGS, **CSV_KWARGS})
    def load_csv(
        self,
        scenario_directory_path: Union[pathlib.Path, str],
        *,
        sep: Optional[str] = None,
        encoding: str = "utf-8",
        process_quotes: bool = True,
        truncate: bool = False,
        watch: bool = False,
        array_sep: Optional[str] = None,
        pattern: Optional[str] = None,
        base_scenario_directory: str = BASE_SCENARIO,
    ):
        """Load multiple CSV files into the store while automatically generating scenarios.

        Loads the data from a directory into multiple scenarios, creating them as necessary, based on the directory's structure.
        The contents of each sub-directory of the provided path will be loaded into a scenario with the same name.
        Here is an example of a valid directory structure:

        .. code-block:: none

                    ScenarioStore
                    ├── Base
                    │   └── base_data.csv
                    ├── Scenario1
                    │   └── scenario1_data.csv
                    └── Scenario2
                    │    └── scenario2_data.csv

        With this structure:

        * The contents of the ``Base`` directory are loaded into the base scenario.
        * Two new scenarios are created: ``Scenario1`` and ``Scenario2``, containing respectively
          the data from ``scenario1_data.csv`` and ``scenario2_data.csv``.

        Args:
            scenario_directory_path: The path pointing to the directory containing all of the scenarios.
            {sep}
            {encoding}
            {process_quotes}
            {truncate}
            {watch}
            {array_sep}
            pattern: A glob pattern used to specify which files to load in each scenario directory.
                If no pattern is provided, all files with the ``.csv`` extension will be loaded by default.
            base_scenario_directory: The data from a scenario directory with this name will be loaded into the base scenario and not a new scenario with the original name of the directory.
        """
        _validate_csv_path(scenario_directory_path)
        pattern = _validate_glob_pattern(pattern) if pattern else None

        MultiScenarioCsvDataSource(self._java_api).load_scenarios_from_csv(
            scenario_directory_path,
            self._store.name,
            base_scenario_directory,
            truncate,
            watch,
            sep,
            encoding,
            process_quotes,
            array_sep,
            pattern,
        )
