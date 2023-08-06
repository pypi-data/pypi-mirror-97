from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
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
    Tuple,
    Union,
)

import pandas as pd

from ._ipython_utils import running_in_ipython
from ._local_cube import LocalCube
from ._providers import PartialAggregateProvider
from ._repr_utils import ReprJson, ReprJsonable
from ._type_utils import BASE_SCENARIO, ScenarioName
from .aggregates_cache import AggregatesCache
from .exceptions import AtotiJavaException
from .hierarchies import Hierarchies
from .level import Level
from .levels import Levels
from .measure import Measure
from .measures import Measures
from .query._cellset import LevelCoordinates
from .simulation import Simulation
from .simulations import Simulations
from .store import Column
from .stores import _GRAPHVIZ_MESSAGE
from .type import INT, DataType

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .session import Session
    from .store import Store

BucketRows = Union[Dict[Tuple[Any, ...], Dict[str, Any]], pd.DataFrame, List[List[Any]]]


class Cube(LocalCube[Hierarchies, Levels, Measures]):
    """Cube of a Session."""

    def __init__(
        self, java_api: JavaApi, name: str, base_store: Store, session: Session
    ):
        """Init."""
        super().__init__(
            name,
            java_api,
            session,
            Hierarchies(java_api, self),
            lambda hierarchies: Levels(hierarchies),
            Measures(java_api, self),
            AggregatesCache(java_api, self),
        )
        self._base_store = base_store
        self._simulations = Simulations(java_api)
        self._shared_context = CubeContext(java_api, self)

    @property
    def simulations(self) -> Simulations:  # noqa: D401
        """Simulations of the cube."""
        return self._simulations

    @property
    def schema(self) -> Any:
        """Schema of the cube's stores as an SVG graph.

        Note:
            Graphviz is required to display the graph.
            It can be installed with Conda: ``conda install graphviz`` or by following the `download instructions <https://www.graphviz.org/download/>`_.

        Returns:
            An SVG image in IPython and a Path to the SVG file otherwise.
        """
        try:
            path = self._java_api.generate_cube_schema_image(self.name)
            if running_in_ipython():
                from IPython.display import SVG

                return SVG(filename=path)
            return Path(path)
        except AtotiJavaException:
            logging.getLogger("atoti.cube").warning(_GRAPHVIZ_MESSAGE)

    @property
    def shared_context(self) -> CubeContext:
        """Context values shared by all the users.

        Context values can also be set at query time, and per user, directly from the UI.
        The values in the shared context are the default ones for all the users.

        - ``queriesTimeLimit``

            The number of seconds after which a running query is cancelled and its resources reclaimed.
            Set to ``-1`` to remove the limit.
            Defaults to 30s.

        - ``queriesResultLimit.intermediateSize``

            The limit number of point locations for a single intermediate result.
            This works as a safe-guard to prevent queries from consuming too much memory, which is especially useful when going to production with several simulatenous users on the same server.
            Set to ``-1`` to use the maximum limit.
            In atoti, the maximum limit is the default while in Atoti+ it defaults to ``1000000``.

        - ``queriesResultLimit.tansientResultSize``

            Similar to ``intermediateSize`` but across all the intermediate results of the same query.
            Set to ``-1`` to use the maximum limit.
            In atoti, the maximum limit is the default while in Atoti+ it defaults to ``10000000``.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> store = session.read_pandas(
            ...     df, keys=["City"], store_name="shared_context example"
            ... )
            >>> cube = session.create_cube(store)
            >>> cube.shared_context["queriesTimeLimit"] = 60
            >>> cube.shared_context["queriesResultLimit.intermediateSize"] = 1000000
            >>> cube.shared_context["queriesResultLimit.transientSize"] = 10000000
            >>> cube.shared_context
            {'queriesTimeLimit': '60', 'queriesResultLimit.intermediateSize': '1000000', 'queriesResultLimit.transientSize': '10000000'}

        """
        return self._shared_context

    @property
    def _aggregate_providers(self) -> List[PartialAggregateProvider]:
        """Get the partial aggregate providers."""
        return self._java_api.get_aggregate_providers(self)

    @_aggregate_providers.setter
    def _aggregate_providers(self, providers: List[PartialAggregateProvider]):
        """Set the partial aggregate providers."""
        self._java_api.set_aggregate_providers(self, providers)
        self._java_api.refresh_pivot()

    def _join_distributed_cluster(
        self, distributed_session_url: str, distributed_cube_name: str
    ):
        """Join the distributed cluster at the given address for the given distributed cube."""

        self._java_api.join_distributed_cluster(
            self, distributed_session_url, distributed_cube_name
        )
        self._java_api.refresh_pivot()

    def _get_level_data_types(
        self, levels_coordinates: Collection[LevelCoordinates]
    ) -> Mapping[LevelCoordinates, str]:
        return {
            level_coordinates: (
                "object"
                if level_coordinates == ("Epoch", "Epoch", "Branch")
                else self.levels[level_coordinates].data_type.java_type
            )
            for level_coordinates in levels_coordinates
        }

    def _get_level_from_identifier(self, identifier: str) -> Level:
        """Get a level from its identifier."""
        [level, hierarchy, dimension] = identifier.split("@")
        return self.levels[(dimension, hierarchy, level)]

    def setup_simulation(
        self,
        name: str,
        *,
        base_scenario: str = BASE_SCENARIO,
        levels: Optional[Sequence[Level]] = None,
        multiply: Optional[Collection[Measure]] = None,
        replace: Optional[Collection[Measure]] = None,
        add: Optional[Collection[Measure]] = None,
    ) -> Simulation:
        """Create a simulation store for the given measures.

        Simulations can have as many scenarios as desired.

        The same measure cannot be passed in several methods.

        Args:
            name: The name of the simulation.
            base_scenario: The name of the base scenario.
            levels: The levels to simulate on.
            multiply: Measures whose values will be multiplied.
            replace: Measures whose values will be replaced.
            add: Measures whose values will be added (incremented).

        Returns:
            The simulation on which scenarios can be made.
        """
        simulation = Simulation(
            name,
            levels or [],
            multiply or [],
            replace or [],
            add or [],
            ScenarioName(base_scenario),
            self,
            self._java_api,
        )
        self.simulations[name] = simulation
        return simulation

    # Make public when we'll have more use cases
    # to know if this is the right design.
    def _setup_bucketing(
        self,
        name: str,
        # Why is this named columns while it's a sequence of levels?
        columns: Sequence[Level],
        *,
        # Would be better not to accept this parameter and
        # let users add data through the regular API of the returned store.
        rows: BucketRows = None,  # type: ignore
        bucket_dimension: str = "Buckets",
        weight_name: Optional[str] = None,
        weighted_measures: Optional[Sequence[Measure]] = None,
    ) -> Store:
        """Create a bucketing store.

        The bucketing is done by mapping one or several columns to buckets with weights.
        This mapping is done in a store with all the columns of the mapping, a column with the bucket and a column for the weight:

            +---------+---------+---------+-----------+------------------+
            | Column1 | Column2 | Column3 | My Bucket | My Bucket_weight |
            +=========+=========+=========+===========+==================+
            | a       | b       | c       | BucketA   |             0.25 |
            +---------+---------+---------+-----------+------------------+
            | a       | b       | c       | BucketB   |             0.75 |
            +---------+---------+---------+-----------+------------------+
            | d       | e       | f       | BucketA   |              1.0 |
            +---------+---------+---------+-----------+------------------+
            | g       | h       | i       | BucketB   |              1.0 |
            +---------+---------+---------+-----------+------------------+

        There are multiple ways to feed this store

        * with a pandas DataFrame corresponding to the store
        * with a list of the rows::

            [
                ["a", "b", "c", "BucketA", 0.25],
                ["a", "b", "c", "BucketB", 0.75],
                ...
            ]

        * with a dict::

            {
                ("a", "b", "c") : {"BucketA": 0.25, "BucketB": 0.75},
                ("d", "e", "f") : {"BucketA": 1.0},
                ...
            }

        Some measures can be overriden automatically to be scaled with the weights.

        Args:
            name: The name of the bucket.
                It will be used as the name of the column in the bucket store and as the name of the bucket hierarchy.
            columns: The columns to bucket on.
            weighted_measures: Measures that will be scaled with the weight.
            rows: The mapping between the columns and the bucket.
                It can either be a list of rows, or a pandas DataFrame.
            bucket_dimension: The name of the dimension to put the bucket hierarchy in.
            weight_name: The name of the measure for the weights.

        Returns:
            The store that can be modified to change the bucketing dynamically.
        """
        from .store import Store  # pylint: disable=redefined-outer-name

        if rows is None:
            rows = [[]]
        if weight_name is None:
            weight_name = name + "_weight"
        if weighted_measures is None:
            weighted_measures = []

        bucket_store_name = self._java_api.create_bucketing(
            self, name, columns, rows, bucket_dimension, weight_name, weighted_measures
        )

        bucket_store = Store(bucket_store_name, self._java_api)

        # We need to refresh the DS and the cube
        self._java_api.refresh(force_start=False)

        if isinstance(rows, pd.DataFrame):
            bucket_store.load_pandas(rows)

        return bucket_store

    def create_store_column_parameter_hierarchy(self, name: str, column: Column):
        """Create a single level static hierarchy which takes its members from a column."""
        self._java_api.create_analysis_hierarchy(
            self,
            name,
            column._store.name,  # pylint: disable=protected-access
            column.name,
        )
        self._java_api.refresh_pivot()

    def create_static_parameter_hierarchy(
        self,
        name: str,
        members: Sequence[Any],
        *,
        data_type: Optional[DataType] = None,
        index_measure: Optional[str] = None,
        indices: Optional[Sequence[int]] = None,
        store_name: Optional[str] = None,
    ):
        """Create an arbitrary single-level static hierarchy with the given members.

        It can be used as a parameter hierarchy in advanced analyses.

        Args:
            name: The name of hierarchy and its single level.
            members: The members of the hierarchy.
            data_type: The type with which the members will be stored.
                Automatically inferred by default.
            index_measure: The name of the indexing measure to create for this hierarchy, if any.
            indices: The custom indices for each member in the new hierarchy.
                They are used when accessing a member through the ``index_measure``.
                Defaults to ``range(len(members))``.
            store_name: The name of the store backing the parameter hierarchy.
                Defaults to the passed ``name`` argument.
        """
        index_column = f"{name}__index"

        indices = list(range(len(members))) if not indices else indices
        parameter_df = pd.DataFrame({name: members, index_column: indices})

        types = {index_column: INT}
        if data_type:
            types[name] = data_type
        elif all(
            isinstance(member, int) and -(2 ** 31) <= member < 2 ** 31
            for member in members
        ):
            types[name] = INT

        store_name = store_name if store_name is not None else name
        parameter_store = self._session.read_pandas(  # type: ignore
            parameter_df,
            store_name,
            keys=[name],
            types=types,
            hierarchized_columns=[name],  # index must not be hierarchized
        )

        self._base_store.join(parameter_store, mapping={})

        if index_measure:
            self.measures[index_measure] = parameter_store[index_column]

        self.hierarchies[store_name, name].slicing = True

        self._java_api.refresh_pivot()


@dataclass(frozen=True)
class CubeContext(MutableMapping[str, str], ReprJsonable):

    _java_api: JavaApi = field(repr=False)
    _cube: Cube = field(repr=False)

    def _get_values(self) -> Mapping[str, str]:
        return self._java_api.get_shared_context_values(self._cube.name)

    def __getitem__(self, key: str) -> str:
        return self._get_values()[key]

    def __setitem__(self, key: str, value: Any):
        self._java_api.set_shared_context_value(self._cube.name, key, str(value))
        self._java_api.refresh_pivot()

    def __delitem__(self, key: str) -> None:
        raise ValueError("Cannot delete context value.")

    def __iter__(self):
        return iter(self._get_values())

    def __len__(self) -> int:
        return len(self._get_values())

    def _ipython_key_completions_(self) -> Sequence[str]:
        return list(self._get_values().keys())

    def __str__(self) -> str:
        return str(self._get_values())

    def __repr__(self) -> str:
        return repr(self._get_values())

    def _repr_json_(self) -> ReprJson:
        return (
            self._get_values(),
            {"expanded": True, "root": "Shared Context Values"},
        )
