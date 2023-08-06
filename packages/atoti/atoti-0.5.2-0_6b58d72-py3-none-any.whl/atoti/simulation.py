from __future__ import annotations

import collections
import pathlib
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

import pandas as pd

from ._docs_utils import (
    CSV_KWARGS,
    HEAD_DOC,
    SIMULATION_APPEND_DOC,
    STORE_IADD_DOC,
    STORE_SHARED_KWARGS,
    doc,
)
from ._file_utils import _split_csv_path_and_pattern
from ._ipython_utils import ipython_key_completions_for_mapping
from ._pandas_utils import get_csv_sep_for_pandas_read_load, pandas_to_temporary_csv
from ._repr_utils import ReprJson, ReprJsonable
from ._sources.csv import CsvDataSource
from ._type_utils import BASE_SCENARIO, ScenarioName
from .store import Row
from .type import DataType

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .cube import Cube, Measure
    from .level import Level

_DEFAULT_PRIORITY = 0

_PRIORITY = "Priority"

_SCENARIO_DOC_KWARGS = {
    "expected_columns": """The expected columns are :attr:`columns` or :attr:`columns_without_priority`.

        The name of the scenario is automatically added before the row is added to the
        simulation store.

        If the value of a column is left empty (``None``), then it will be treated as a wildcard
        value. i.e. it will match all the values of the corresponding column when performing the
        simulation.
        """,
    "what": "scenario",
}

_SIMULATION_DOC_KWARGS = {
    "expected_columns": """The expected columns are :attr:`columns` or :attr:`columns_without_priority`.

        The value provided for ``simulation_name`` is the name of the scenario the values will be loaded into.

        If the value of a column is left empty (``None``), then it will be treated as a wildcard value, meaning that it will match all the values of the corresponding column when performing the simulation.
        """
}


@dataclass
class Simulation(ReprJsonable):
    """Represents a simulation."""

    _name: str
    _levels: Sequence[Level]
    _multiply: Collection[Measure]
    _replace: Collection[Measure]
    _add: Collection[Measure]
    _base_scenario: ScenarioName
    _cube: Cube = field(repr=False)
    _java_api: JavaApi = field(repr=False)

    def __post_init__(self):
        """Finish the initialization."""
        mul: List[str] = [m.name for m in self._multiply]
        rep: List[str] = [m.name for m in self._replace]
        add: List[str] = [m.name for m in self._add]

        measure_count = len(mul) + len(rep) + len(add)
        if measure_count == 0:
            raise ValueError("At least one measure is required to define a simulation")
        if len(set(mul + rep + add)) != measure_count:
            raise ValueError(
                "Some measures are present in more than one method."
                "Only use one method per measure"
            )

        # pylint: disable=attribute-defined-outside-init
        self._scenarios = SimulationScenarios(self)
        self._underlying_scenarios: Set[ScenarioName] = {self._base_scenario}
        self._measure_columns = (
            [self.name + "_" + measure.name + "_multiply" for measure in self._multiply]
            + [self.name + "_" + measure.name + "_replace" for measure in self._replace]
            + [self.name + "_" + measure.name + "_add" for measure in self._add]
        )
        # pylint: enable=attribute-defined-outside-init

        self._java_api.do_create_simulation(
            self._cube,
            self.name,
            self.levels,
            self._multiply,
            self._replace,
            self._add,
            self._base_scenario,
        )
        self._java_api.refresh()

    @property
    def columns(self) -> Sequence[str]:
        """Columns of the simulation."""
        return (
            [lvl.name for lvl in self.levels]
            + [self.name]
            + self.measure_columns
            + [_PRIORITY]
        )

    @property
    def _types(self) -> Mapping[str, DataType]:
        """Columns of the simulation and their types."""
        return {
            col.name: DataType(col.column_type_name, col.is_nullable)
            for col in self._java_api.get_store_schema(self)
        }

    @property
    def columns_without_priority(self) -> Sequence[str]:
        """Columns of the simulation (Priority column excluded)."""
        return [column for column in self.columns if column != _PRIORITY]

    @property
    def levels(self) -> Sequence[Level]:
        """Levels of the simulation."""
        return self._levels

    @property
    def measure_columns(self) -> List[str]:
        """Measure columns of the simulation."""
        return self._measure_columns

    @property
    def name(self) -> str:
        """Name of the simulation."""
        return self._name

    @property
    def scenarios(self) -> SimulationScenarios:
        """Scenarios of the simulation."""
        return self._scenarios

    @doc(HEAD_DOC, what="simulation")
    def head(self, n: int = 5) -> pd.DataFrame:
        if n < 1:
            raise ValueError("n must be at least 1.")

        dataframe = self._java_api.get_store_dataframe(self, n)
        # Remove the BASE scenario row
        dataframe = dataframe[dataframe[self.name] != self._base_scenario]
        dataframe = dataframe.set_index(
            keys=[level.name for level in self.levels] + [self.name]
        )
        return dataframe

    @doc(
        **{**STORE_SHARED_KWARGS, **CSV_KWARGS, **_SIMULATION_DOC_KWARGS},
    )
    def load_csv(
        self,
        path: Union[pathlib.Path, str],
        *,
        sep: Optional[str] = None,
        encoding: str = "utf-8",
        process_quotes: bool = True,
        watch: bool = False,
        array_sep: Optional[str] = None,
    ):
        """Load a CSV into this simulation.

        {expected_columns}

        If a value for a specific field is left empty, it wil be treated as a wildcard value, meaning that it will match all the values of the corresponding column when performing the simulation.

        Args:
            {path}
            {sep}
            {encoding}
            {process_quotes}
            {watch}
            {array_sep}
        """
        path, pattern = _split_csv_path_and_pattern(path)
        CsvDataSource(self._java_api).load_csv_into_store(
            path,
            self,
            BASE_SCENARIO,
            True,
            sep,
            encoding,
            process_quotes,
            False,
            watch,
            array_sep,
            pattern,
        )
        return self

    @doc(**{**STORE_SHARED_KWARGS, **_SIMULATION_DOC_KWARGS})
    def load_pandas(self, dataframe: pd.DataFrame, **kwargs: Any):  # type: ignore
        """Load a pandas DataFrame into this simulation.

        {expected_columns}

        If the value of a column is left empty (``None``), it will be treated as a wildcard value, meaning that it will match all the values of the corresponding column when performing the simulation.

        Args:
            dataframe: The DataFrame to load.
        """
        # create the expected columns
        lvl_names = [lvl.name for lvl in self.levels]
        columns = lvl_names + [self.name, _PRIORITY] + self.measure_columns

        df_columns = list(dataframe.columns.values)
        if collections.Counter(columns) != collections.Counter(df_columns):
            raise ValueError(
                f"The DataFrame's columns are incorrect. \n Expected {columns}"
                f"but got {df_columns}"
            )

        # set sep to | because can contains list with sep , [x, y, ...]
        sep, kwargs = get_csv_sep_for_pandas_read_load(kwargs)
        csv_file, _ = pandas_to_temporary_csv(dataframe, sep)

        return self.load_csv(csv_file, sep=sep, **kwargs)

    def _repr_json_(self) -> ReprJson:
        schema: Dict[str, Any] = {
            "Levels": [lvl.name for lvl in self.levels],
            "Scenarios": list(self._underlying_scenarios),
        }

        if self._add:
            schema["add"] = [m.name for m in self._add]
        if self._multiply:
            schema["multiply"] = [m.name for m in self._multiply]
        if self._replace:
            schema["replace"] = [m.name for m in self._replace]

        return schema, {"expanded": True, "root": self.name}


@dataclass(frozen=True)
class Scenario:
    """A scenario for a simulation."""

    name: str
    """Name of the scenario."""

    _simulation: Simulation
    _java_api: JavaApi = field(repr=False)

    @property
    def columns(self) -> Sequence[str]:
        """Columns of the scenario."""
        return [
            column
            for column in self._simulation.columns
            if column != self._simulation.name
        ]

    @property
    def columns_without_priority(self) -> Sequence[str]:
        """Columns of the scenario (Priority column excluded)."""
        return [column for column in self.columns if column != _PRIORITY]

    @doc(**_SCENARIO_DOC_KWARGS)
    def load_csv(self, path: Union[pathlib.Path, str], *, sep: Optional[str] = ","):
        """Load a CSV into this scenario.

        {expected_columns}

        If a value for a column on a given row is empty, it will be treated as a wildcard, meaning that it will match all the values of the corresponding column when performing the simulation.

        Args:
            path: The path to the CSV file.
            sep: The CSV separator character.
                If ``None``, it is inferred by pandas.
        """
        dataframe = pd.read_csv(path, sep=sep)
        return self.load_pandas(dataframe)

    @doc(**_SCENARIO_DOC_KWARGS)
    def load_pandas(self, dataframe: pd.DataFrame, **kwargs):  # type: ignore
        """Load a pandas DataFrame into this scenario.

        {expected_columns}

        Args:
            dataframe: The DataFrame to load.
        """
        # Shallow copy the passed DataFrame to avoid mutating it.
        dataframe = dataframe.copy()

        # Create the expected column names
        lvl_names = [lvl.name for lvl in self._simulation.levels]
        columns = (
            lvl_names
            + [self._simulation.name, _PRIORITY]
            + self._simulation.measure_columns
        )

        # Check the column names are correct
        df_columns = list(dataframe.columns.values)
        if collections.Counter(columns) != collections.Counter(df_columns):
            columns = lvl_names + [_PRIORITY] + self._simulation.measure_columns
            if collections.Counter(columns) == collections.Counter(df_columns):
                dataframe[self._simulation.name] = self.name
            else:
                raise ValueError(
                    f" The DataFrame's columns are incorrect.\n"
                    f"Expected {columns} but got {df_columns}"
                )

        # set sep to | because can contains list with sep , [x, y, ...]
        sep, kwargs = get_csv_sep_for_pandas_read_load(kwargs)

        # Save pandas as CSV then read it
        csv_file, _ = pandas_to_temporary_csv(dataframe, sep)

        self._simulation.load_csv(csv_file, sep=sep, **kwargs)
        return self

    def _prepare_mapping(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        """Clean and prepare the data in a row for the Java API."""
        # Shallow copy the passed row to avoid mutating it.
        prepared_row = {**row}

        if self._simulation.name not in prepared_row:
            prepared_row[self._simulation.name] = self.name
        if _PRIORITY.lower() in prepared_row and _PRIORITY in prepared_row:
            raise ValueError(
                f"'{_PRIORITY.lower()}' and '{_PRIORITY}' cannot both be used as column names."
            )
        if _PRIORITY.lower() in prepared_row:
            prepared_row[_PRIORITY] = prepared_row.pop(_PRIORITY.lower())
        if _PRIORITY in prepared_row:
            priority = prepared_row[_PRIORITY]
            # Check that the value provided for the priority is a number.
            if not isinstance(priority, (int, float)):
                raise ValueError(
                    f"Value {priority} provided for {_PRIORITY} is of incorect type, "
                    f"expected a number but got {type(priority)}"
                )
        else:
            prepared_row[_PRIORITY] = _DEFAULT_PRIORITY

        if not (len(prepared_row.keys())) == len(self._simulation.levels) + 2 + len(
            self._simulation.measure_columns
        ):
            raise ValueError(
                f"Incorrect number of columns in row {prepared_row}.\n"
                f"Got {len(prepared_row.keys())}, expected "
                f"{len(self._simulation.levels) + 2 + len(self._simulation.measure_columns)}"
            )

        return prepared_row

    def _prepare_tuple(self, row: Tuple[Any, ...]) -> Row:
        """Clean and prepare the data in a row for the Java API."""
        required_values_count = len(self._simulation.levels) + len(
            self._simulation.measure_columns
        )
        required_values_and_priority_count = required_values_count + 1
        if len(row) < required_values_count:
            raise ValueError(
                f"Provided row does not contain enough values, got {len(row)},"
                f"expected {required_values_count} or {required_values_and_priority_count} values"
            )
        row_dict = {}
        for level in self._simulation.levels:
            row_dict[level.name] = row[len(row_dict)]
        for measure_column in self._simulation.measure_columns:
            row_dict[measure_column] = row[len(row_dict)]
        if len(row) == required_values_and_priority_count:
            row_dict[_PRIORITY] = row[len(row_dict)]
        return self._prepare_mapping(row_dict)

    @doc(SIMULATION_APPEND_DOC, **_SCENARIO_DOC_KWARGS)
    def append(self, *rows: Row):
        prepare_func = (
            self._prepare_mapping
            if isinstance(rows[0], Mapping)
            else self._prepare_tuple
        )
        prepared_rows = [prepare_func(cast(Any, row)) for row in rows]
        self._java_api.insert_multiple_in_store(
            self._simulation, BASE_SCENARIO, prepared_rows, True
        )

    @doc(STORE_IADD_DOC, **_SCENARIO_DOC_KWARGS)
    def __iadd__(self, row: Row):
        self.append(row)
        return self

    @doc(HEAD_DOC, **_SCENARIO_DOC_KWARGS)
    def head(self, n: int = 5) -> pd.DataFrame:
        if n < 1:
            raise ValueError("n must be at least 1.")
        dataframe = self._java_api.get_store_dataframe(
            self._simulation,
            0,
            keys=[
                level.name
                for level in self._simulation.levels  # pylint: disable=protected-access
            ],
        )
        # reset the index so the row numbers are coherent
        dataframe = dataframe[dataframe[self._simulation.name] == self.name].drop(
            columns=self._simulation.name
        )
        return dataframe.head(n)


@dataclass(frozen=True)
class SimulationScenarios(MutableMapping[str, Scenario]):
    """Manage the scenarios of a simulation."""

    _simulation: Simulation

    def __contains__(self, key: str) -> bool:
        """Return whether the scenario exists in the simulation or not.

        Args:
            key: The name of the scenario
        """
        return key in self._simulation._underlying_scenarios

    def __getitem__(self, key: str) -> Scenario:
        """Get the scenario or create it if it does not exist.

        Args:
            key: The name of the new scenario
        """
        scenario = Scenario(key, self._simulation, self._simulation._java_api)
        if key not in self:
            self._simulation._underlying_scenarios.add(ScenarioName(key))
        return scenario

    def __setitem__(
        self, key: str, value: Union[Scenario, int, float, List[int], List[float]]
    ) -> Scenario:
        """Override __setitem__ to allow immediate assignment.

        This allows to call methods on the underlying scenario directly after assignment, because the default Python implementation of this method does not return the value.

        Args:
            key: The name of the scenario
            value: The value of the scenario
        """
        if key == self._simulation._base_scenario:
            raise ValueError(
                f"You cannot edit the {self._simulation._base_scenario} scenario."
            )
        if isinstance(value, Scenario):
            return value
        if isinstance(value, (int, float, list)) and not isinstance(value, bool):
            # Exclude bool because bool extends int.
            if (
                len(self._simulation.levels) == 0
                and len(self._simulation.measure_columns) == 1
            ):
                new_scenario = self[key]
                new_scenario += (value,)
                return new_scenario
            raise ValueError(
                "You can only assign a value directly to a scenario for simulation with no fields."
            )
        raise ValueError(
            f"You cannot assign a value of type: {type(value)} to a scenario"
        )

    def __delitem__(self, key: str) -> None:
        """Delete the scenario with the given name."""
        if key in self._simulation._underlying_scenarios:
            self._simulation._java_api.delete_simulation_scenario(self._simulation, key)
            self._simulation._underlying_scenarios.remove(ScenarioName(key))
        else:
            raise KeyError(f"No scenario named {key}")

    def __iter__(self):
        """Return the iterator on the scenarios of the simulation."""
        return iter(self._simulation._underlying_scenarios)

    def __len__(self) -> int:
        """Return the number of scenarios in the simulation."""
        return len(self._simulation._underlying_scenarios)

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self)
