from __future__ import annotations

import json
import warnings
from dataclasses import asdict, dataclass
from types import FunctionType
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

import pandas as pd
from typing_extensions import Literal

from ._endpoint import PyApiEndpoint
from ._measures.utils import convert_level_in_description
from ._path_utils import PathLike, _is_cloud_path, to_absolute_path
from ._providers import PartialAggregateProvider
from ._py4j_utils import (
    to_java_map,
    to_java_map_list,
    to_java_object_array,
    to_java_object_array_array,
    to_java_object_list,
    to_java_string_array,
    to_python_dict,
    to_python_list,
)
from ._query_plan import QueryAnalysis, QueryPlan, RetrievalData
from ._type_utils import Port, ScenarioName
from ._vendor.atotipy4j.clientserver import (
    ClientServer,
    JavaParameters,
    PythonParameters,
)
from ._vendor.atotipy4j.java_collections import JavaArray, JavaMap, ListConverter
from .comparator import Comparator
from .config._session_configuration import SessionConfiguration
from .exceptions import _java_api_call_wrapper
from .hierarchy import Hierarchy
from .level import Level
from .report import LoadingReport, _warn_new_errors
from .sampling import SamplingMode
from .type import DataType, _is_temporal

if TYPE_CHECKING:
    from ._local_cube import BucketRows, LocalCube, _LocalCube
    from ._local_cubes import LocalCubes
    from ._local_session import LocalSession
    from .config._role import Restrictions
    from .cube import Cube
    from .measure import Measure
    from .named_measure import NamedMeasure
    from .simulation import Simulation
    from .store import Row, Store

DataFrameDescription = Tuple[List[str], Sequence[Sequence[Any]]]


def _parse_detailed_type(underlying_type: str) -> DataType:
    """Parse java detailed type string in DataType."""
    clean_type = underlying_type.replace("nullable ", "")
    clean_type = (
        clean_type
        if clean_type not in ["Boolean", "String", "Object"]
        # .lower() since java detailed type sometimes start with Upper or Lower case.
        else clean_type.lower()
    )
    return (
        DataType(clean_type, True)
        if "nullable " in underlying_type
        else DataType(clean_type, False)
    )


class ApiMetaClass(type):
    """Meta class for the API calls."""

    def __new__(
        cls, classname: str, bases: Tuple[type, ...], class_dict: Dict[str, Any]
    ):
        """Automatically wrap all of the classes methods.

        This class applies the api_call_wrapper to all of a particular classes methods.
        This allows for cleaner handling of Py4J related exceptions.
        """
        new_class_dict = {}
        for attribute_name, attribute in class_dict.items():
            if isinstance(attribute, FunctionType):
                attribute = _java_api_call_wrapper(attribute)
            new_class_dict[attribute_name] = attribute
        return type.__new__(cls, classname, bases, new_class_dict)


# pylint: disable=too-many-lines
class JavaApi(metaclass=ApiMetaClass):
    """API for communicating with the JVM."""

    def __init__(
        self, *, py4j_java_port: Optional[Port] = None, distributed: bool = False
    ):
        """Create the Java gateway."""
        self.gateway = JavaApi._create_py4j_gateway(py4j_java_port)
        self.java_session: Any = self.gateway.entry_point
        self.java_api = self.java_session.api(distributed)

    @staticmethod
    def _create_py4j_gateway(java_port: Optional[Port] = None) -> ClientServer:
        # Connnect to the Java side using the provided Java port
        # and start the Python callback server with a dynamic port.
        gateway = ClientServer(
            java_parameters=JavaParameters(port=java_port),
            python_parameters=PythonParameters(daemonize=True, port=0),
        )

        # Retrieve the port on which the python callback server was bound to.
        cb_server = gateway.get_callback_server()
        if cb_server is None:
            raise ValueError("Null callback server from py4j gateway")
        python_port = cb_server.get_listening_port()

        # Tell the Java side to connect to the Python callback server with the new Python port.
        gateway_server = gateway.java_gateway_server
        if gateway_server is None:
            raise ValueError("Null gateway server from py4j gateway")
        # ignore type next line because we do some Java calls
        gateway_server.resetCallbackClient(
            gateway_server.getCallbackClient().getAddress(), python_port  # type: ignore
        )

        return gateway

    def shutdown(self):
        """Shutdown the connection to the Java gateway."""
        self.gateway.shutdown()

    def refresh(self, *, force_start: bool = False, check_errors: bool = True):
        """Refresh the Java session.

        Args:
            force_start: start the dataStore without stopping it.
            check_errors: check the loading errors.

        """
        self.java_session.refresh(force_start)
        if check_errors:
            _warn_new_errors(self.get_new_load_errors())

    def refresh_pivot(self):
        """Refresh the pivot."""
        self.java_api.refreshPivot()
        _warn_new_errors(self.get_new_load_errors())

    def clear_session(self):
        """Refresh the pivot."""
        self.java_api.clearSession()

    def start_feeding(self):
        """Start feeding if necessary."""
        self.java_api.startFeeding()
        _warn_new_errors(self.get_new_load_errors())

    def get_session_port(self) -> int:
        """Return the port of the session."""
        return self.java_session.getPort()

    def get_session_url(self) -> str:
        """Return the URL of the session."""
        return self.java_session.getPublicUrl()

    def get_throwable_root_cause(self, throwable: Any) -> str:
        """Get the root cause of a java exception."""
        return self.java_api.getRootCause(throwable)

    def generate_jwt(self) -> str:
        """Return the JWT required to authenticate against to this session."""
        return self.java_session.generateJwt()

    def create_endpoint(
        self,
        route: str,
        custom_endpoint: PyApiEndpoint,
        http_method: Literal["POST", "GET", "PUT", "DELETE"],
        session_url: str,
    ):
        """Create a new custom endpoint."""
        self.java_api.createEndpoint(
            route,
            custom_endpoint,
            http_method,
            session_url,
        )

    def configure_session(self, config: SessionConfiguration):
        self.java_api.configureSession(json.dumps(asdict(config)))

    def _convert_restriction(self, restrictions: Restrictions) -> JavaMap:
        """Convert a restriction to a Java map."""
        restr = dict()
        for (field, restriction) in restrictions.items():
            members = restriction if isinstance(restriction, list) else [restriction]
            restr[field] = ListConverter().convert(
                members, self.gateway._gateway_client
            )
        return to_java_map(self.gateway, restr)

    def _convert_role_mapping(
        self, mapping: Optional[Mapping[str, Optional[Collection[str]]]]
    ) -> JavaMap:
        """Convert a role mapping to java object."""
        if mapping is None:
            return to_java_map(self.gateway, dict())
        role_mapping = {
            name: ListConverter().convert(role, self.gateway._gateway_client)
            for (name, role) in mapping.items()
        }
        return to_java_map(self.gateway, role_mapping)

    def set_locale(self, locale: str):
        """Set the locale to use for the session."""
        self.java_api.setLocale(locale)

    def export_i18n_template(self, path: PathLike):
        """Generate a template translations file at the desired location."""
        self.java_api.exportI18nTemplate(to_absolute_path(path))

    def start_application(self):
        """Start the application."""
        self.java_api.startSession()

    def _create_java_types(self, types: Mapping[str, DataType]) -> Any:
        """Convert the python types to java types."""
        # pylint: disable=invalid-name
        atoti_package = self.gateway.jvm.io.atoti  # type: ignore
        JavaColumnType: Any = atoti_package.loading.impl.TypeImpl  # type: ignore
        Pair: Any = self.gateway.jvm.com.quartetfs.fwk.impl.Pair  # type: ignore
        # pylint: enable=invalid-name
        converted = [
            Pair(field, JavaColumnType(type_value.java_type, type_value.nullable))
            for (field, type_value) in types.items()
        ]
        return to_java_object_list(self.gateway, converted)

    def get_stores(self) -> List[str]:
        """List all the stores of the session."""
        return to_python_list(self.java_api.getStores())

    def _java_sampling_mode(self, mode: SamplingMode) -> Any:
        """Convert the sampling mode to a Java sampling mode."""
        params = ListConverter().convert(mode.parameters, self.gateway._gateway_client)
        atoti_package: Any = self.gateway.jvm.io.atoti  # type: ignore
        sampling_class: Any = atoti_package.loading.sampling.StoreSamplingPolicy  # type: ignore
        return sampling_class.get(mode.name, params)

    def create_store_params(
        self,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        sampling: SamplingMode,
        hierarchized_columns: Optional[Collection[str]],
    ) -> Any:
        """Create the store parameters."""
        java_keys = (
            ListConverter().convert(keys, self.gateway._gateway_client)
            if keys
            else None
        )
        if types is None:
            types = dict()
        java_types = self._create_java_types(types)
        java_sampling = self._java_sampling_mode(sampling)
        java_hierarchized_columns = (
            ListConverter().convert(hierarchized_columns, self.gateway._gateway_client)
            if hierarchized_columns is not None
            else None
        )
        package: Any = self.gateway.jvm.io.atoti.loading.impl  # type: ignore
        params = package.StoreParams(
            java_keys,
            partitioning,
            java_types,
            java_sampling,
            java_hierarchized_columns,
        )
        return params

    def create_loading_params(
        self,
        scenario_name: Optional[ScenarioName],
        in_all_scenarios: bool,
        watch: bool,
        truncate: bool,
        is_cloud_path: bool,
    ) -> Any:
        """Create the loading parameters."""
        package: Any = self.gateway.jvm.io.atoti.loading.impl  # type: ignore
        cache_cloud_files = False
        if is_cloud_path:
            cache_cloud_files = self.java_api.getCacheCloudFiles()
            if cache_cloud_files and watch:
                warnings.warn(
                    "Caching of watched cloud files is not supported. These watched files will not be cached.",
                    stacklevel=2,
                )
                cache_cloud_files = False
        params = package.LoadingParams(
            None, in_all_scenarios, watch, truncate, cache_cloud_files
        )
        if scenario_name is not None:
            params.setBranch(scenario_name)
        return params

    def create_store(
        self,
        schema: Mapping[str, DataType],
        store_name: str,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        sampling_mode: SamplingMode,
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a java store from its schema."""
        store_params = self.create_store_params(
            keys, partitioning, schema, sampling_mode, hierarchized_columns
        )
        self.java_api.createStore(store_name, store_params)

    def convert_source_params(self, params: Mapping[str, Any]) -> Any:
        """Convert the params to Java Objects."""
        java_params = {}
        for param in params:
            value = params[param]
            if isinstance(value, list):
                value = to_java_object_list(self.gateway, value)
            elif isinstance(value, dict):
                value = to_java_map(self.gateway, value)
            java_params[param] = value
        return to_java_map(self.gateway, java_params)

    def create_store_from_source(
        self,
        store_name: str,
        source_key: str,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        sampling: SamplingMode,
        in_all_scenarios: bool,
        watch: bool,
        source_params: Mapping[str, Any],
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a store with the given source."""
        store_params = self.create_store_params(
            keys, partitioning, types, sampling, hierarchized_columns
        )
        load_params = self.create_loading_params(
            None,
            in_all_scenarios,
            watch,
            False,
            _is_cloud_path(str(source_params.get("path", ""))),
        )
        source_params = self.convert_source_params(source_params)
        self.java_api.createStoreFromDataSource(
            store_name, source_key, store_params, load_params, source_params
        )

    def load_data_into_store(
        self,
        store_name: str,
        source_key: str,
        scenario_name: Optional[ScenarioName],
        in_all_scenarios: bool,
        watch: bool,
        truncate: bool,
        source_params: Mapping[str, Any],
    ):
        """Load the data into an existing store with a given source."""
        load_params = self.create_loading_params(
            scenario_name,
            in_all_scenarios,
            watch,
            truncate,
            _is_cloud_path(str(source_params.get("path", ""))),
        )
        source_params = self.convert_source_params(source_params)
        self.java_api.loadDataSourceIntoStore(
            store_name, source_key, load_params, source_params
        )
        # Check if errors happened during the loading
        _warn_new_errors(self.get_new_load_errors())

    def create_scenario(self, scenario: ScenarioName, parent_scenario: ScenarioName):
        """Create a new scenario on the store."""
        self.java_api.createBranch(scenario, parent_scenario)

    def get_scenarios(self) -> List[str]:
        """Get the list of scenarios defined in the current session."""
        return to_python_list(self.java_api.getBranches())

    def delete_scenario(self, scenario: ScenarioName):
        """Delete a scenario from the store."""
        self.java_api.deleteBranch(scenario)

    def start_transaction(self):
        """Start a multi operation transaction on the datastore."""
        self.java_api.startTransaction()

    def end_transaction(self, has_succeeded: bool):
        """End a multi operation transaction on the datastore."""
        self.java_api.endTransaction(has_succeeded)

    @dataclass(frozen=True)
    class AggregatesCacheDescription:
        """Aggregates cache description."""

        capacity: int

    def get_aggregates_cache_description(
        self, cube: LocalCube[Any, Any, Any]
    ) -> JavaApi.AggregatesCacheDescription:
        """Return the description of the aggregates cache associated with a given cube."""
        jcache_desc = self.java_api.getAggregatesCacheDescription(cube.name)
        return JavaApi.AggregatesCacheDescription(capacity=jcache_desc.getSize())

    def set_aggregates_cache(self, cube: LocalCube[Any, Any, Any], capacity: int):
        """Set the aggregates cache description for a given cube."""
        self.java_api.setAggregatesCache(cube.name, capacity)

    def _convert_partial_provider(self, provider: PartialAggregateProvider) -> Any:
        """Convert the partial provider to the Java Object."""
        # pylint: disable=protected-access
        levels = ListConverter().convert(
            [lvl._java_description for lvl in provider.levels],
            self.gateway._gateway_client,
        )
        # pylint: enable=protected-access
        measures = ListConverter().convert(
            [meas.name for meas in provider.measures],
            self.gateway._gateway_client,
        )
        java_class: Any = self.gateway.jvm.io.atoti.api.impl.PythonPartialProvider  # type: ignore
        return java_class(provider.key, levels, measures)

    def get_aggregate_providers(self, cube: Cube) -> List[PartialAggregateProvider]:
        """Get the partial aggregates providers."""
        java_providers = self.java_api.getPartialAggregateProviders(cube.name)
        # pylint: disable=protected-access
        return [
            PartialAggregateProvider(
                provider.getKey(),
                [
                    cube._get_level_from_identifier(lvl)
                    for lvl in to_python_list(provider.getLevels())
                ],
                [
                    cube.measures[measure_name]
                    for measure_name in to_python_list(provider.getMeasures())
                ],
            )
            for provider in to_python_list(java_providers)
        ]
        # pylint: enable=protected-access

    def set_aggregate_providers(
        self,
        cube: Cube,
        providers: List[PartialAggregateProvider],
    ):
        """Set the partial aggregate providers."""
        java_providers = ListConverter().convert(
            [self._convert_partial_provider(provider) for provider in providers],
            self.gateway._gateway_client,
        )
        self.java_api.setPartialAggregateProviders(cube.name, java_providers)

    def join_distributed_cluster(
        self, cube: Cube, distributed_session_url: str, distributed_cube_name: str
    ):
        """Join the distributed cluster at the given address for the given distributed cube."""
        self.java_api.setDistributedCubeConfiguration(
            cube.name, distributed_session_url, distributed_cube_name
        )

    @dataclass(frozen=True)
    class ColumnDescription:
        """Store column description."""

        name: str
        column_type_name: str
        is_nullable: bool

    # https://github.com/Microsoft/pyright/issues/104 -> Unbound variables not detected
    def get_store_schema(self, store: Union[Store, Simulation]) -> List[JavaApi.ColumnDescription]:  # type: ignore
        """Return the schema of the java store."""
        schema = self.java_api.getStoreSchema(store.name)
        columns_descr = []
        for i in range(0, len(list(schema.fieldNames()))):
            columns_descr.append(
                JavaApi.ColumnDescription(
                    schema.fieldNames()[i],
                    schema.types()[i].literalType().getParser(),
                    schema.types()[i].nullable(),
                )
            )
        return columns_descr

    def get_store_partitioning(self, store: Store) -> str:
        """Return the store's partitioning."""
        return self.java_api.getStorePartitioning(store.name)

    @staticmethod
    def _convert_reports(reports: Any) -> List[LoadingReport]:
        """Convert the Java report to Python ones."""
        return [
            LoadingReport(
                r.getName(),
                r.getType(),
                r.getLoadedCount(),
                r.getFailureCount(),
                r.getDuration(),
                to_python_list(r.getFailureMessages()),
            )
            for r in to_python_list(reports)
        ]

    def get_loading_report(self, store: Store) -> List[LoadingReport]:
        """Return the loading report of the store."""
        reports = self.java_api.getLoadingReports(store.name)
        return self._convert_reports(reports)

    def get_new_load_errors(self) -> Dict[str, int]:
        """Return the new loading errors per store."""
        errors = self.java_api.getNewLoadingErrors()
        return to_python_dict(errors)

    def set_source_simulation_enabled(self, store: Store, enabled: bool) -> None:
        """Set the sourceSimulationEnabled property of a store."""
        self.java_api.setSourceSimulationEnabledOnStore(store.name, enabled)

    def get_source_simulation_enabled(self, store: Store) -> bool:
        """Get the value of the sourceSimulationEnabled property of a store."""
        return self.java_api.getSourceSimulationEnabledOnStore(store.name)

    def get_key_columns(self, store: Store) -> Sequence[str]:
        """Return the list of key columns for the store."""
        java_columns = self.java_api.getKeyFields(store.name)
        return to_python_list(java_columns)

    def get_selection_fields(self, cube: Cube) -> Sequence[str]:
        """Return the list of fields that are part of the cube's datastore selection."""
        java_fields = self.java_api.getSelectionFields(cube.name)
        return to_python_list(java_fields)

    def create_cube_from_store(
        self,
        store: Store,
        cube_name: str,
        creation_mode: str,
    ):
        """Create a cube from a given store."""
        self.java_api.createCubeFromStore(store.name, cube_name, creation_mode)

    def create_distributed_cube(self, cube_name: str):
        """Create a distributed cube."""
        self.java_api.createDistributedCube(cube_name)

    def generate_cube_schema_image(self, cube_name: str) -> str:
        """Generate the cube schema image and return its path."""
        return self.java_api.getCubeSchemaPath(cube_name)

    def generate_datastore_schema_image(self) -> str:
        """Generate the datastore schema image and return its path."""
        return self.java_api.getDatastoreSchemaPath()

    def delete_cube(self, cube_name: str) -> None:
        """Delete a cube from the current session."""
        self.java_api.deleteCube(cube_name)

    def create_join(
        self,
        store: Store,
        other_store: Store,
        mappings: Optional[Mapping[str, str]],
    ):
        """Define a join between two stores."""
        # Convert mappings.
        jmappings = (
            to_java_map(self.gateway, mappings) if mappings is not None else mappings
        )

        self.java_api.createReferences(store.name, other_store.name, jmappings)

    def get_store_size(self, store: Store) -> int:
        """Get the size of the store on its current scenario."""
        self.start_feeding()
        return self.java_api.getStoreSize(store.name, store.scenario)

    def insert_multiple_in_store(
        self,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        rows: Sequence[Row],
        in_all_scenarios: bool,
    ) -> None:
        """Insert multiple rows on a store scenario."""
        scenario = None if in_all_scenarios else scenario_name
        # Check the type of the row
        if isinstance(rows[0], dict):
            # We assume the all the other elements are dicts
            jrows = []
            for row in rows:
                row = cast(dict, row)
                jrows.append(to_java_map(self.gateway, row))
            jmap_rows = ListConverter().convert(jrows, self.gateway._gateway_client)
            self.java_api.insertMultipleOnStoreBranch(
                store.name, scenario, in_all_scenarios, jmap_rows
            )
        elif isinstance(rows[0], tuple):
            obj_obj_arr = to_java_object_array_array(self.gateway, rows)
            self.java_api.insertMultipleOnStoreBranch(
                store.name, scenario, in_all_scenarios, obj_obj_arr
            )

    def delete_rows_from_store(
        self,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        coordinates: Sequence[Mapping[str, Any]],
        in_all_scenarios: bool,
    ) -> None:
        """Delete rows from the store matching the provided coordinates."""
        scenario = None if in_all_scenarios else scenario_name
        jcoordinates = [
            to_java_map(self.gateway, column_values) for column_values in coordinates
        ]
        jcoordinates_list = ListConverter().convert(
            jcoordinates, self.gateway._gateway_client
        )
        self.java_api.deleteOnStoreBranch(
            store.name, scenario, jcoordinates_list, in_all_scenarios
        )

    def get_store_dataframe(
        self,
        store: Union[Store, Simulation],
        rows: int,
        scenario_name: Optional[ScenarioName] = None,
        keys: Optional[Sequence[str]] = None,
    ) -> pd.DataFrame:
        """Return the first given rows of the store as a pandas DataFrame."""
        self.start_feeding()
        dfrh = self.java_api.dataFrameRowsAndHeaders(store.name, scenario_name, rows)

        headers = to_python_list(dfrh.getHeader())
        content = to_python_list(dfrh.getRows())
        dataframe = pd.DataFrame(data=content, columns=headers).apply(
            pd.to_numeric, errors="ignore"
        )

        for name, data_type in store._types.items():  # pylint: disable=protected-access
            # Convert dates to Python object
            if _is_temporal(data_type):
                dataframe[name] = dataframe[name].apply(to_date)

        if keys:
            dataframe.set_index(keys, inplace=True)

        return dataframe

    @staticmethod
    def _convert_from_java_levels(jlevels: Any) -> Dict[str, Level]:
        """Convert from java levels."""
        jlevels_dict = to_python_dict(jlevels)
        levels = {}
        for (name, jlvl) in jlevels_dict.items():
            comparator_name = jlvl.getComparatorName()
            first_members = (
                list(jlvl.getFirstMembers())
                if jlvl.getFirstMembers() is not None
                else None
            )
            if comparator_name is None:
                comparator = None
            else:
                comparator = Comparator(comparator_name, first_members)
            levels[name] = Level(
                name,
                jlvl.getPropertyName(),
                _parse_detailed_type(jlvl.getDetailType()),
                _comparator=comparator,
            )
        return levels

    def create_or_update_hierarchy(
        self,
        cube: LocalCube[Any, Any, Any],
        dimension: str,
        hierarchy_name: str,
        levels: Mapping[str, Level],
    ):
        """Create a hierarchy on a cube, or update the level of an existing hierarchy."""
        level_names = list(levels.keys())
        column_names = [
            level._column_name  # pylint: disable=protected-access
            for level in levels.values()
        ]
        self.java_api.createHierarchyForCube(
            cube.name,
            dimension,
            hierarchy_name,
            ListConverter().convert(level_names, self.gateway._gateway_client),
            ListConverter().convert(column_names, self.gateway._gateway_client),
        )

    def create_analysis_hierarchy(
        self, cube: Cube, name: str, store_name: str, column_name: str
    ):
        """Create an analysis hierarchy from an existing store column."""
        self.java_api.createAnalysisHierarchy(
            cube.name,
            name,
            store_name,
            column_name,
        )

    def create_date_hierarchy(
        self,
        cube: Cube,
        store: Store,
        field: str,
        hierarchy_name: str,
        levels: Mapping[str, str],
    ):
        pair: Any = self.gateway.jvm.com.quartetfs.fwk.impl.Pair  # type: ignore
        converted = [pair(name, pattern) for (name, pattern) in levels.items()]
        levels_list = to_java_object_list(self.gateway, converted)
        self.java_api.createDateHierarchy(
            cube.name,
            store.name,
            field,
            hierarchy_name,
            levels_list,
        )

    def update_hierarchy_coordinate(
        self,
        cube: LocalCube[Any, Any, Any],
        hierarchy: Hierarchy,
        new_dim: str,
        new_hier: str,
    ):
        """Change the coordinate of a hierarchy."""
        # pylint: disable=protected-access
        self.java_api.updateHierarchyCoordinate(
            cube.name, hierarchy._java_description, f"{new_hier}@{new_dim}"
        )

    def update_hierarchy_slicing(self, hierarchy: Hierarchy, slicing: bool):
        """Update whether the hierarchy is slicing or not."""
        # pylint: disable=protected-access
        self.java_api.setHierarchySlicing(
            hierarchy._cube.name, hierarchy._java_description, slicing
        )

    def update_level_comparator(self, level: Level):
        """Change the level comparator."""
        # pylint: disable=protected-access
        comparator_name = (
            level.comparator._name if level.comparator is not None else None
        )
        first_members = None
        if level.comparator is not None and level.comparator._first_members is not None:
            first_members = to_java_object_array(
                self.gateway, level.comparator._first_members
            )

        if level._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {level.name}.")

        self.java_api.updateLevelComparator(
            level._hierarchy._cube.name,
            level._java_description,
            comparator_name,
            first_members,
        )
        # pylint: enable=protected-access

    def drop_level(self, level: Level):
        """Delete a level."""
        # pylint: disable=protected-access
        hier = level._hierarchy
        if hier is None:
            raise ValueError("No hierarchy for level " + level.name)
        self.java_api.deleteLevel(hier._cube.name, level._java_description)

    def drop_hierarchy(self, cube: LocalCube[Any, Any, Any], hierarchy: Hierarchy):
        """Drop a hierarchy from the cube."""
        # pylint: disable=protected-access
        self.java_api.dropHierarchy(cube.name, hierarchy._java_description)

    def retrieve_cubes(
        self, session: LocalSession[LocalCubes[_LocalCube]]
    ) -> Mapping[str, _LocalCube]:
        """Retrieve the cubes of the session."""
        from .cube import Cube
        from .experimental.distributed.cube import DistributedCube
        from .experimental.distributed.session import DistributedSession
        from .session import Session

        java_cubes = self.java_api.retrieveCubes()
        if isinstance(session, Session):
            return {
                java_cube.getName(): Cube(
                    self,
                    java_cube.getName(),
                    session.stores[java_cube.getStoreName()],
                    session,
                )
                for java_cube in to_python_list(java_cubes)
            }  # type: ignore
        if isinstance(session, DistributedSession):
            return {
                java_cube.getName(): DistributedCube(self, java_cube.getName(), session)
                for java_cube in to_python_list(java_cubes)
            }  # type: ignore
        raise ValueError(f"""Failed to retrieve cubes from session "{session.name}".""")

    def retrieve_cube(
        self, cube_name: str, session: LocalSession[LocalCubes[_LocalCube]]
    ) -> _LocalCube:
        """Retrieve a cube of the session using its name."""
        from .cube import Cube
        from .experimental.distributed.cube import DistributedCube
        from .experimental.distributed.session import DistributedSession
        from .session import Session

        java_cube = self.java_api.retrieveCube(cube_name)
        if isinstance(session, Session):
            return Cube(
                self,
                java_cube.getName(),
                session.stores[java_cube.getStoreName()],
                session,
            )  # type: ignore
        if isinstance(session, DistributedSession):
            return DistributedCube(self, java_cube.getName(), session)  # type: ignore
        raise ValueError(
            f"""Failed to retrieve cube "{cube_name}" from session "{session.name}"."""
        )

    def retrieve_hierarchies(
        self, cube: LocalCube[Any, Any, Any]
    ) -> Mapping[Tuple[str, str], Hierarchy]:
        """Retrieve the hierarchies of the cube."""
        hierarchies: Dict[Tuple[str, str], Hierarchy] = {}
        java_hierarchies = self.java_api.retrieveHierarchies(cube.name)
        python_hierarchies = self._convert_to_python_hierarchies(
            cube, to_python_dict(java_hierarchies).values()
        )
        for hierarchy in python_hierarchies:
            hierarchies[(hierarchy.dimension, hierarchy.name)] = hierarchy
        return hierarchies

    def retrieve_hierarchy(
        self, cube: LocalCube[Any, Any, Any], dimension: Optional[str], name: str
    ) -> List[Hierarchy]:
        """Retrieve a cube's hierarchy."""
        # Get the hierarchy from the java side.
        java_hierarchies = to_python_list(
            self.java_api.retrieveHierarchy(cube.name, dimension, name)
        )

        return self._convert_to_python_hierarchies(cube, java_hierarchies)

    def retrieve_hierarchy_for_level(
        self,
        cube: LocalCube[Any, Any, Any],
        dimension_name: Optional[str],
        hierarchy_name: Optional[str],
        level_name: str,
    ) -> List[Hierarchy]:
        """Retrieve the hierarchy containing a level with the given name."""
        java_hierarchies = to_python_list(
            self.java_api.retrieveHierarchyForLevel(
                cube.name, dimension_name, hierarchy_name, level_name
            )
        )
        return self._convert_to_python_hierarchies(cube, java_hierarchies)

    def _convert_to_python_hierarchies(
        self, cube: LocalCube[Any, Any, Any], java_hierarchies: Any
    ) -> List[Hierarchy]:
        """Convert java hierarchies to python ones."""
        hierarchies = []
        for java_hierarchy in java_hierarchies:
            hierarchy = Hierarchy(
                java_hierarchy.getName(),
                JavaApi._convert_from_java_levels(java_hierarchy.getLevels()),
                java_hierarchy.getDimensionName(),
                java_hierarchy.getSlicing(),
                cube,
                self,
                java_hierarchy.getVisible(),
            )
            for level in hierarchy.levels.values():
                level._hierarchy = hierarchy  # pylint: disable=protected-access
            hierarchies.append(hierarchy)
        return hierarchies

    def set_hierarchy_visibility(
        self,
        cube: LocalCube[Any, Any, Any],
        dimension: Optional[str],
        name: str,
        visible: bool,
    ):
        self.java_api.setHierarchyVisibility(cube.name, dimension, name, visible)

    def set_measure_folder(
        self, cube_name: str, measure: Measure, folder: Optional[str]
    ):
        """Set the folder of a measure."""
        self.java_api.setMeasureFolder(cube_name, measure.name, folder)

    def set_measure_formatter(
        self, cube_name: str, measure: Measure, formatter: Optional[str]
    ):
        """Set the formatter of a measure."""
        self.java_api.setMeasureFormatter(cube_name, measure.name, formatter)

    def set_visible(self, cube_name: str, measure: Measure, visible: Optional[bool]):
        """Set the visibility of a measure."""
        self.java_api.setMeasureVisibility(cube_name, measure.name, visible)

    def set_measure_description(
        self, cube_name: str, measure: NamedMeasure, description: Optional[str]
    ):
        """Set the measure description."""
        self.java_api.setMeasureDescription(cube_name, measure.name, description)

    @dataclass(frozen=True)
    class MeasureDescription:
        """Description of a measure to build."""

        folder: str
        formatter: str
        visible: bool
        underlying_type: DataType
        description: Optional[str]

    def get_full_measures(
        self, cube: LocalCube[Any, Any, Any]
    ) -> Dict[str, JavaApi.MeasureDescription]:
        """Retrieve the list of the cube's measures, including their required levels."""
        java_measures = self.java_api.getFullMeasures(cube.name)
        measures = to_python_list(java_measures)
        final_measures: Dict[str, JavaApi.MeasureDescription] = {}
        for measure in measures:
            final_measures[measure.getName()] = JavaApi.MeasureDescription(
                measure.getFolder(),
                measure.getFormatter(),
                measure.isVisible(),
                _parse_detailed_type(measure.getType()),
                measure.getDescription(),
            )
        return final_measures

    def get_measure(
        self, cube: LocalCube[Any, Any, Any], measure_name: str
    ) -> JavaApi.MeasureDescription:
        """Retrieve all the details about a measure defined in the cube."""
        measure = self.java_api.getMeasure(cube.name, measure_name)
        return JavaApi.MeasureDescription(
            measure.getFolder(),
            measure.getFormatter(),
            measure.isVisible(),
            _parse_detailed_type(measure.getType()),
            measure.getDescription(),
        )

    def get_required_levels(self, measure: NamedMeasure) -> List[str]:
        """Get the required levels of a measure."""
        # pylint: disable=protected-access
        return to_python_list(
            self.java_api.getRequiredLevels(measure._cube.name, measure.name)
        )
        # pylint: enable=protected-access

    @staticmethod
    def create_retrieval(jretr: Any) -> RetrievalData:
        """Convert Java retrieval to Python."""
        loc_str = ", ".join(
            [
                str(loc.getDimension())
                + "@"
                + str(loc.getHierarchy())
                + "@"
                + "\\".join(to_python_list(loc.getLevel()))
                + ": "
                + "\\".join(str(x) for x in to_python_list(loc.getPath()))
                for loc in to_python_list(jretr.getLocation())
            ]
        )
        timings = to_python_dict(jretr.getTimingInfo())
        return RetrievalData(
            id=jretr.getRetrId(),
            retrieval_type=jretr.getType(),
            location=loc_str,
            filter_id=jretr.getFilterId(),
            measures=to_python_list(jretr.getMeasures()),
            start_times=list(timings.get("startTime", [])),
            elapsed_times=list(timings.get("elapsedTime", [])),
            result_size=jretr.getResultSize(),
            retrieval_filter=str(jretr.getFilterId()),
            partitioning=jretr.getPartitioning(),
            measures_provider=jretr.getMeasureProvider(),
        )

    @staticmethod
    def create_query_plan(jplan: Any) -> QueryPlan:
        """Create a query plan."""
        jinfos = jplan.getPlanInfo()
        infos = {
            "ActivePivot": {
                "Type": jinfos.getPivotType(),
                "Id": jinfos.getPivotId(),
                "Branch": jinfos.getBranch(),
                "Epoch": jinfos.getEpoch(),
            },
            "Cube filters": {
                f.getId(): f.getDescription()
                for f in to_python_list(jplan.getQueryFilters())
            },
            "Continuous": jinfos.isContinuous(),
            "Range sharing": jinfos.getRangeSharing(),
            "Missed prefetches": jinfos.getMissedPrefetchBehavior(),
            "Cache": jinfos.getAggregatesCache(),
            "Global timings (ms)": to_python_dict(jinfos.getGlobalTimings()),
        }
        retrievals = [
            JavaApi.create_retrieval(plan)
            for plan in to_python_list(jplan.getRetrievals())
        ]
        dependencies = {
            key: to_python_list(item)
            for key, item in to_python_dict(jplan.getDependencies()).items()
        }
        return QueryPlan(infos, retrievals, dependencies)

    def analyse_mdx(self, mdx: str, timeout: int) -> QueryAnalysis:
        """Analyse an MDX query on a given cube."""
        jplans = to_python_list(self.java_api.analyseMdx(mdx, timeout))
        plans = [
            JavaApi.create_query_plan(jplan)
            for jplan in jplans
            if jplan.getPlanInfo().getClass().getSimpleName() == "PlanInfoData"
        ]
        return QueryAnalysis(plans)

    def copy_measure(self, cube_name: str, copied_measure: Measure, new_name: str):
        """Copy a measure."""
        self.java_api.copyMeasure(cube_name, copied_measure.name, new_name)

    def create_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        measure_plugin_key: str,
        *args: Any,
    ):
        """Create a new measure with by giving its constructor arguments."""
        return self.java_api.createMeasure(
            cube.name,
            measure_name,
            measure_plugin_key,
            to_java_object_array(
                self.gateway, [self.levels_to_descriptions(arg) for arg in args]
            ),
        )

    def levels_to_descriptions(self, arg: Any) -> Any:
        """Recursively convert levels and hierarchies to their java descriptions."""
        if isinstance(arg, Level):
            return arg._java_description  # pylint: disable=protected-access
        if isinstance(arg, Hierarchy):
            return arg._java_description  # pylint: disable=protected-access
        if isinstance(arg, Tuple):
            return to_java_object_array(
                self.gateway, tuple(self.levels_to_descriptions(e) for e in arg)
            )
        if isinstance(arg, Mapping):
            return to_java_map(
                self.gateway,
                {
                    self.levels_to_descriptions(k): self.levels_to_descriptions(v)
                    for k, v in arg.items()
                },
            )
        if isinstance(arg, (List, Set)):
            return ListConverter().convert(
                [self.levels_to_descriptions(e) for e in arg],
                self.gateway._gateway_client,  # pylint: disable=protected-access
            )
        return arg

    def aggregated_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        store_name: str,
        column_name: str,
        agg_function: str,
        required_levels: Optional[Collection[Level]],
    ) -> str:
        """Create a new aggregated measure and return its name."""
        java_required_levels = (
            to_java_string_array(
                self.gateway, convert_level_in_description(required_levels)
            )
            if required_levels is not None
            else None
        )
        return self.java_api.aggregatedMeasure(
            cube.name,
            measure_name,
            store_name,
            column_name,
            agg_function,
            java_required_levels,
        )

    def not_measure(
        self, cube: Cube, measure_name: Optional[str], underlying_name: str
    ) -> str:
        """Create a new inverted boolean measure and return its name."""
        return self.java_api.notMeasure(cube.name, measure_name, underlying_name)

    def array_element_at(
        self,
        cube_name: str,
        measure_name: Optional[str],
        array_measure: Measure,
        index_measure: Measure,
        levels: Collection[str],
    ) -> str:
        """Create a measure equal to the element at the given index of an array measure and return its name."""
        array_name = array_measure.name
        index_name = index_measure.name
        jlevels = to_java_string_array(self.gateway, levels)
        return self.java_api.getVectorElement(
            cube_name, measure_name, array_name, index_name, jlevels
        )

    def delete_measure(self, cube: Cube, measure_name: str) -> bool:
        """Delete a mesure and return ``True`` if the measure has been found and deleted."""
        return self.java_api.deleteMeasure(cube.name, measure_name)

    def min_member(
        self, cube: Cube, measure_name: Optional[str], underlying: str, level: Level
    ) -> str:
        """Create the min member measure and return its name."""
        return self.java_api.minMember(
            cube.name,
            measure_name,
            underlying,
            level._java_description,  # pylint: disable=protected-access
        )

    def max_member(
        self, cube: Cube, measure_name: Optional[str], underlying: str, level: Level
    ) -> str:
        """Create the max member measure and return its name."""
        return self.java_api.maxMember(
            cube.name,
            measure_name,
            underlying,
            level._java_description,  # pylint: disable=protected-access
        )

    def do_create_simulation(
        self,
        cube: Cube,
        simulation_name: str,
        columns: Sequence[Level],
        multiply: Collection[Measure],
        replace: Collection[Measure],
        add: Collection[Measure],
        base_scenario_name: ScenarioName,
    ):
        """Create a family of simulatinos for the cube and return the name of its backing store."""
        # Replace None values
        if not multiply:
            multiply = []
        if not replace:
            replace = []
        if not add:
            add = []

        # Convert to java objects
        jmultiply = to_java_string_array(
            self.gateway, [measure.name for measure in multiply]
        )
        jreplace = to_java_string_array(
            self.gateway, [measure.name for measure in replace]
        )
        jadd = to_java_string_array(self.gateway, [measure.name for measure in add])
        jcolumns = to_java_string_array(
            self.gateway, convert_level_in_description(columns)
        )
        self.java_api.doCreateSimulation(
            cube.name,
            simulation_name,
            jcolumns,
            jmultiply,
            jreplace,
            jadd,
            base_scenario_name,
        )

    def delete_simulation_scenario(
        self, simulation: Simulation, scenario_name: str
    ) -> None:
        """Delete a scenario from the given simulation."""
        self.java_api.deleteScenario(simulation.name, scenario_name)

    def _get_java_rows_for_bucketing(
        self,
        # Contains pd.DataFrame which is untyped.
        rows: BucketRows,  # type: ignore
    ) -> JavaArray:
        """Convert the rows to the expected format for bucketing."""
        if isinstance(rows, list):
            java_rows = to_java_object_array_array(self.gateway, rows)
        elif isinstance(rows, dict):
            converted_rows = []
            for column_values, value in rows.items():
                for bucket, weight in value.items():
                    row: List[Any] = list(column_values)
                    row.append(bucket)
                    row.append(weight)
                    converted_rows.append(row)
            java_rows = to_java_object_array_array(self.gateway, converted_rows)
        elif isinstance(rows, pd.DataFrame):
            # Insertion is done after store creation.
            java_rows = to_java_object_array_array(self.gateway, [])
        else:
            raise ValueError("Rows are not in the expected format.")
        return java_rows

    def create_bucketing(
        self,
        cube: Cube,
        bucket_name: str,
        columns_seq: Sequence[Level],
        # Contains pd.DataFrame which is untyped.
        rows_for_bucket: BucketRows,  # type: ignore
        bucket_dimension: str,
        weight_name: str,
        weighted_measures: Sequence[Measure],
    ) -> str:
        """Create a new bucketing on a cube and return the name of its backing store."""
        jrows = self._get_java_rows_for_bucketing(rows_for_bucket)
        jlevels = to_java_string_array(
            self.gateway,
            [
                lvl._java_description  # pylint: disable=protected-access
                for lvl in columns_seq
            ],
        )
        jweighted_measures = ListConverter().convert(
            [m.name for m in weighted_measures], self.gateway._gateway_client
        )
        return self.java_api.createBucketing(
            cube.name,
            bucket_name,
            jlevels,
            jrows,
            bucket_dimension,
            weight_name,
            jweighted_measures,
        )

    def delete_simulation(self, simulation: Simulation) -> None:
        """Delete the given simulation from the JVM."""
        self.java_api.deleteSimulation(simulation.name)

    def block_until_widget_loaded(self, wiget_id: str) -> bool:
        """Block until the widget is loaded or the JupyterLab extension is found unresponsive."""
        return self.java_api.blockUntilWidgetLoaded(wiget_id)

    def get_shared_context_values(self, cube_name: str) -> Mapping[str, str]:
        return to_python_dict(self.java_api.getCubeShareContextValues(cube_name))

    def set_shared_context_value(self, cube_name: str, key: str, value: str):
        self.java_api.setCubeSharedContextValue(cube_name, key, value)

    def get_sampling_mode(self, store: Store) -> SamplingMode:
        """Get the sampling mode of the given store."""
        java_mode = self.java_api.getSamplingMode(store.name)
        return SamplingMode(java_mode.getMode(), list(java_mode.getParameters()))

    def should_warn_for_store_sampling_policy(self, store: Store) -> bool:
        """Check whether we should warn because a store does not respect the policy."""
        return self.java_api.shouldWarnForSamplingPolicy(store.name)

    def load_all_data(self):
        """Trigger the full loading mode."""
        self.java_api.triggerFullLoad()

    def set_branding_directory(self, branding_directory: str):
        """Set branding directory."""
        self.java_api.setBrandingDirectory(branding_directory)

    def setup_app_form(
        self,
        name: str,
        action: str,
        inputs: Mapping[str, Mapping[str, Union[bool, float, int, str]]],
    ):
        """Set up app form."""
        self.java_api.setupAppForm(
            name,
            action,
            to_java_map_list(
                self.gateway,
                [
                    {**properties, **{"name": name}}
                    for name, properties in inputs.items()
                ],
            ),
        )


def to_date(value: Any) -> Any:
    """Convert a Java date to a Python one."""
    try:
        if pd.isna(value):  # raises TypeError for JavaMember
            return None
    except TypeError:
        pass
    try:
        return pd.to_datetime(value.toString())
    except Exception:  # pylint: disable=broad-except
        return value
