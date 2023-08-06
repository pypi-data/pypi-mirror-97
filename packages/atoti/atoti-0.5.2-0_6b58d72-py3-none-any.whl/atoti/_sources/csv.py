from __future__ import annotations

from typing import TYPE_CHECKING, Any, Collection, Dict, Mapping, Optional, Union

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..sampling import SamplingMode
    from ..simulation import Simulation
    from ..store import Store
    from ..type import DataType


def create_csv_params(
    path: PathLike,
    sep: Optional[str],
    encoding: str,
    process_quotes: Optional[bool],
    array_sep: Optional[str],
    pattern: Optional[str],
) -> Dict[str, Any]:
    """Create the CSV spefic parameters."""
    return {
        "path": to_absolute_path(path),
        "separator": sep,
        "encoding": encoding,
        "processQuotes": process_quotes,
        "arraySeparator": array_sep,
        "pattern": pattern,
    }


class CsvDataSource(DataSource):
    """CSV data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "CSV")

    def create_store_from_csv(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Collection[str]],
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
        sampling: SamplingMode,
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a Java store from a CSV file or directory."""
        source_params = create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.create_store_from_source(
            store_name,
            keys,
            partitioning,
            types,
            sampling,
            in_all_scenarios,
            watch,
            source_params,
            hierarchized_columns,
        )

    def load_csv_into_store(
        self,
        path: PathLike,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: bool,
        truncate: bool,
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a csv into an existing store."""
        source_params = create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.load_data_into_store(
            store.name,
            scenario_name,
            in_all_scenarios,
            watch,
            truncate,
            source_params,
        )


class MultiScenarioCsvDataSource(DataSource):
    """Multi scenarios CSV data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "MULTI_SCENARIO_CSV")

    def load_scenarios_from_csv(
        self,
        scenario_directory_path: PathLike,
        store_name: str,
        base_scenario_directory: str,
        truncate: bool,
        watch: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a directory of CSV files into a store while automatically generating scenarios."""
        source_params = create_csv_params(
            scenario_directory_path, sep, encoding, process_quotes, array_sep, pattern
        )
        source_params["baseFolderName"] = base_scenario_directory
        self.load_data_into_store(
            store_name,
            None,
            False,
            watch,
            truncate,
            source_params,
        )
