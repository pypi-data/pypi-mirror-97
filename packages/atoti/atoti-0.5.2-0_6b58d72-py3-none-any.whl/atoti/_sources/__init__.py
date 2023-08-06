from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Collection, Mapping, Optional

from .._type_utils import ScenarioName

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..sampling import SamplingMode
    from ..type import DataType


class DataSource(ABC):
    """Abstract data source."""

    def __init__(self, java_api: JavaApi, source_key: str):
        """Initialise the source.

        Args:
            java_api: The Java API of the session.
            source_key: The key of the source.
        """
        self._java_api = java_api
        self.source_key = source_key

    def create_store_from_source(
        self,
        store_name: str,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        sampling: SamplingMode,
        in_all_scenarios: bool,
        watch: bool,
        source_params: Mapping[str, Any],
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a store with the given source.

        Args:
            store_name: The name to give to the store.
            keys:  The key columns for the store.
            partitioning: The partitioning description.
            types: Manually specified types.
            sampling: The sammpling mode.
            in_all_scenarios: Whether to load the data in all the scenarios or not.
            watch: Whether to watch the sources or not.
            source_params: The parameters specific to the source.
            hierarchized_columns: The columns to convert into hierarchies
        """
        self._java_api.create_store_from_source(
            store_name,
            self.source_key,
            keys,
            partitioning,
            types,
            sampling,
            in_all_scenarios,
            watch,
            source_params,
            hierarchized_columns,
        )

    def load_data_into_store(
        self,
        store_name: str,
        scenario_name: Optional[ScenarioName],
        in_all_scenarios: bool,
        watch: bool,
        truncate: bool,
        source_params: Mapping[str, Any],
    ):
        """Load the data into an existing store with a given source.

        Args:
            store_name: The name of the store to feed.
            scenario_name: The name of the scenario to feed.
            in_all_scenarios: Whether to load the data in all the scenarios or not.
            watch: Whether to watch the sources or not.
            truncate: Whether the store should be truncated beofre loading the data.
            source_params: The parameters specific to the source.
        """
        self._java_api.load_data_into_store(
            store_name,
            self.source_key,
            scenario_name,
            in_all_scenarios,
            watch,
            truncate,
            source_params,
        )
