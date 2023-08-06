from __future__ import annotations

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import pandas as pd
import pyarrow as pa
from typing_extensions import Literal

from ._arrow import run_raw_arrow_query
from ._base._base_cube import BaseCube
from ._base._base_level import BaseLevel
from ._bitwise_operators_only import IdentityElement
from ._docs_utils import doc
from ._hierarchy_isin_conditions import HierarchyIsInCondition
from ._java_api import JavaApi
from ._level_conditions import LevelCondition
from ._level_isin_conditions import LevelIsInCondition
from ._local_hierarchies import _LocalHierarchies
from ._local_measures import _LocalMeasures
from ._multi_condition import MultiCondition
from ._query_plan import QueryAnalysis
from ._type_utils import BASE_SCENARIO, ScenarioName, typecheck
from .aggregates_cache import AggregatesCache
from .experimental.distributed.levels import DistributedLevels
from .levels import Levels
from .named_measure import NamedMeasure
from .query._cellset import LevelCoordinates
from .query._widget_conversion import WidgetConversionDetails
from .query.cube import _QUERY_ARGS_DOC, _QUERY_DOC, _decombine_condition
from .query.level import QueryLevel
from .query.measure import QueryMeasure
from .query.query_result import QueryResult

if TYPE_CHECKING:
    from ._local_session import LocalSession

_Level = TypeVar("_Level", bound=BaseLevel)
_Levels = TypeVar("_Levels", Levels, DistributedLevels)
_Measure = Union[NamedMeasure, QueryMeasure]

BucketRows = Union[Dict[Tuple[Any, ...], Dict[str, Any]], pd.DataFrame, List[List[Any]]]

_LocalCube = TypeVar("_LocalCube", bound="LocalCube")

_QUERY_ARGS_WITH_MODE_DOC = f"""{_QUERY_ARGS_DOC}
            mode: The query mode.

              * ``"pretty"`` is best for queries returning small results:

                * A :class:`~atoti.query.query_result.QueryResult` will be returned and its rows will be sorted according to the level comparators.
              *  ``"raw"`` is best for benchmarks or large exports:

                * A faster and more efficient endpoint reducing the data transfer from Java to Python will be used.
                * A classic :class:`pandas.DataFrame` will be returned.
                * ``include_totals="True"`` will not be allowed.
                * The :guilabel:`Convert to Widget Below` action provided by the :mod:`atoti-jupyterlab <atoti_jupyterlab>` plugin will not be available.
"""


@typecheck
class LocalCube(BaseCube[_LocalHierarchies, _Levels, _LocalMeasures]):
    """Local cube class."""

    def __init__(
        self,
        name: str,
        java_api: JavaApi,
        session: LocalSession[Any],
        hierarchies: _LocalHierarchies,
        level_function: Callable[[_LocalHierarchies], _Levels],
        measures: _LocalMeasures,
        agg_cache: AggregatesCache,
    ):
        """Init."""
        super().__init__(name, hierarchies, measures)
        self._session = session
        self._java_api = java_api
        self._levels = level_function(hierarchies)
        self._agg_cache = agg_cache

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._name

    @property
    def hierarchies(self) -> _LocalHierarchies:
        """Hierarchies of the cube."""
        return self._hierarchies

    @property
    def levels(self) -> _Levels:
        """Levels of the cube."""
        return self._levels

    @property
    def measures(self) -> _LocalMeasures:
        """Measures of the cube."""
        return self._measures

    @property
    def aggregates_cache(self) -> AggregatesCache:  # noqa: D401
        """Aggregates cache of the cube."""
        return self._agg_cache

    @abstractmethod
    def _get_level_data_types(
        self, levels_coordinates: Collection[LevelCoordinates]
    ) -> Mapping[LevelCoordinates, str]:
        ...

    @doc(_QUERY_DOC, args=_QUERY_ARGS_WITH_MODE_DOC)
    def query(
        self,
        *measures: _Measure,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        include_totals: bool = False,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        mode: Literal["pretty", "raw"] = "pretty",
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> Union[QueryResult, pd.DataFrame]:
        if mode == "pretty":
            (
                mdx,
                widget_conversion_details,
            ) = self._generate_mdx_and_widget_conversion_details(
                condition=condition,
                include_totals=include_totals,
                levels=levels,
                measures=measures,
                scenario=ScenarioName(scenario),
            )
            query_result = self._session.query_mdx(
                mdx, keep_totals=include_totals, timeout=timeout
            )
            # pylint: disable=protected-access
            query_result._atoti_widget_conversion_details = widget_conversion_details
            # pylint: enable=protected-access
            return query_result

        if include_totals:
            raise ValueError("""Totals cannot be included in "raw" mode.""")

        # Raw query
        # Note: Converting to pandas is fast for small tables (<100K) but can take several seconds for large datasets
        return self._query_as_arrow(
            *measures,
            condition=condition,
            levels=levels,
            scenario=scenario,
            timeout=timeout,
        ).to_pandas()

    def _query_as_arrow(
        self,
        *measures: _Measure,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> pa.Table:
        if not measures and levels is None:
            # If nothing is queried return all the visible measures sorted by name
            measures = tuple(
                sorted(
                    (m for m in self.measures.values() if m.visible),
                    key=lambda m: m.name,
                )
            )
        params = {
            "cubeName": self.name,
            "branch": scenario,
            "measures": [m.name for m in measures],
            "levelCoordinates": _get_level_description(levels),
            **_serialize_conditions(condition),
            "timeout": timeout,
        }
        return run_raw_arrow_query(
            params,
            session=self._session._open_transient_query_session(),  # pylint: disable=protected-access
        )

    @doc(args=_QUERY_ARGS_DOC)
    def explain_query(
        self,
        *measures: _Measure,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        include_totals: bool = False,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> QueryAnalysis:
        """Run the query but return an explanation of the query instead of the result.

        The explanation contains a summary, global timings and the query plan with all the retrievals.

        {args}
        """
        mdx, *_ = self._generate_mdx_and_widget_conversion_details(
            condition=condition,
            include_totals=include_totals,
            levels=levels,
            measures=measures,
            scenario=ScenarioName(scenario),
        )
        return self._java_api.analyse_mdx(mdx, timeout)

    def _generate_mdx_and_widget_conversion_details(
        self,
        *,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        include_totals: bool,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        measures: Sequence[_Measure],
        scenario: ScenarioName,
    ) -> Tuple[str, Optional[WidgetConversionDetails]]:
        query_measures = [
            QueryMeasure(
                measure.name,
                measure.visible,
                measure.folder,
                measure.formatter,
                measure.description,
            )
            for measure in measures
        ]
        query_levels = (
            [
                QueryLevel(level.name, level.dimension, level.hierarchy)
                for level in (levels or [])
            ]
            if isinstance(levels, Sequence) or levels is None
            else [QueryLevel(levels.name, levels.dimension, levels.hierarchy)]
        )
        return (
            self._session._open_transient_query_session()  # pylint: disable=protected-access
            .cubes[self.name]
            ._generate_mdx_and_widget_conversion_details(
                condition=condition,
                include_totals=include_totals,
                levels=query_levels,
                measures=query_measures,
                scenario=scenario,
                session=self._session,
            )
        )

    def _identity(self) -> Tuple[IdentityElement, ...]:
        return (
            self._name,
            self._session.name,
        )


def _serialize_conditions(
    condition: Optional[
        Union[
            LevelCondition,
            MultiCondition,
            LevelIsInCondition,
            HierarchyIsInCondition,
        ]
    ]
) -> Dict[str, Any]:
    (
        level_conditions,
        level_isin_condition,
        hierarchy_isin_condition,
    ) = _decombine_condition(condition)

    # Ensure there is no hierarchy conditions
    if hierarchy_isin_condition:
        raise ValueError("Unsupported hierarchy isin condition in raw query mode.")

    # Ensure all condition are == or isin on strings
    # pylint: disable=protected-access
    for lvl_condition in level_conditions:
        if lvl_condition._operation != "eq":
            raise ValueError(
                f"'{lvl_condition._operation}' not supported in query condition: level conditions can only be based on equality (==) or isin."
            )
        if not isinstance(lvl_condition._value, str):
            raise TypeError(
                f"Type {type(lvl_condition._value)} not supported in query condition: level conditions can only be based on equality with strings."
            )
    for isin_condition in level_isin_condition:
        not_string = [
            value for value in isin_condition._members if not isinstance(value, str)
        ]
        if not_string:
            raise TypeError(
                f"Only strings are supported in query condition but the following values are not strings: {str(not_string)}."
            )
    # Serialize the conditions
    lvl_equals = {
        cond._level._java_description: cond._value for cond in level_conditions
    }
    lvl_isin = {
        cond._level._java_description: cond._members for cond in level_isin_condition
    }
    # pylint: enable=protected-access
    return {
        "equalConditions": lvl_equals,
        "isinConditions": lvl_isin,
    }


def _get_level_description(
    levels: Optional[Union[_Level, Sequence[_Level]]] = None
) -> Sequence[str]:
    if levels is None:
        return []
    # pylint: disable=protected-access
    if isinstance(levels, Sequence):
        return [lvl._java_description for lvl in levels]
    return [levels._java_description]
    # pylint: enable=protected-access
