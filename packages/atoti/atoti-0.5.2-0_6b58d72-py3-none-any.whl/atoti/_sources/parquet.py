from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Optional

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..sampling import SamplingMode
    from ..store import Store


class ParquetDataSource(DataSource):
    """Parquet data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "PARQUET")

    def create_store_from_parquet(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Collection[str]],
        in_all_scenarios: bool,
        partitioning: Optional[str],
        sampling: SamplingMode,
        watch: bool,
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a java store from a parquet file."""
        self.create_store_from_source(
            store_name,
            keys,
            partitioning,
            None,
            sampling,
            in_all_scenarios,
            watch,
            {"path": to_absolute_path(path)},
            hierarchized_columns,
        )

    def load_parquet_into_store(
        self,
        path: PathLike,
        store: Store,
        scenario_name: ScenarioName,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        watch: bool = False,
    ):
        """Load a Parquet into an existing store."""
        self.load_data_into_store(
            store.name,
            scenario_name,
            in_all_scenarios,
            watch,
            truncate,
            {"path": to_absolute_path(path)},
        )
