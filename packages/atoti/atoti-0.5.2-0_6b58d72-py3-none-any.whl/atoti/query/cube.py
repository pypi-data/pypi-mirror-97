from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Tuple, Union

from .._base._base_cube import BaseCube
from .._base._base_session import BaseSession
from .._docs_utils import doc
from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._multi_condition import MultiCondition
from .._type_utils import BASE_SCENARIO, ScenarioName
from ._mdx_utils import generate_mdx
from ._widget_conversion import WidgetConversionDetails
from .hierarchies import QueryHierarchies
from .level import QueryLevel
from .levels import QueryLevels
from .measure import QueryMeasure
from .measures import QueryMeasures
from .query_result import QueryResult

if TYPE_CHECKING:
    from .session import QuerySession

_QUERY_ARGS_DOC = """Args:
            measures: The measures to query.
                If ``None``, all the measures are queried.
            condition: The filtering condition.
                Only conditions on level equality with a string are supported.
                For instance:

                * ``lvl["Country"] == "France"``
                * ``(lvl["Country"] == "USA") & (lvl["Currency"] == "USD")``
                * ``h["Geography"].isin(("Asia",), ("Europe", "France"))``
            include_totals: Whether the returned DataFrame should include the grand total and subtotals.
                Totals can be useful but they make the DataFrame harder to work with since its index will have some empty values.
            levels: The levels to split on.
                If ``None``, the value of the measures at the top of the cube is returned.
            scenario: The scenario to query.
            timeout: The query timeout in seconds.
"""


_QUERY_DOC = """Query the cube to retrieve the value of the passed measures on the given levels.

        In JupyterLab with the :mod:`atoti-jupyterlab <atoti_jupyterlab>` plugin installed, query results can be converted to interactive widgets with the :guilabel:`Convert to Widget Below` action available in the command palette or by right clicking on the representation of the returned Dataframe.

        {args}
"""


@dataclass(frozen=True)
class QueryCube(BaseCube[QueryHierarchies, QueryLevels, QueryMeasures]):
    """Query cube."""

    _session: QuerySession = field(repr=False)

    @property
    def levels(self) -> QueryLevels:
        """Levels of the cube."""
        return QueryLevels(self.hierarchies)

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
        levels: Sequence[QueryLevel],
        measures: Sequence[QueryMeasure],
        scenario: ScenarioName,
        session: BaseSession[Any],
    ) -> Tuple[str, Optional[WidgetConversionDetails]]:
        (
            level_conditions,
            level_isin_conditions,
            hierarchy_isin_conditions,
        ) = _decombine_condition(condition)

        mdx = generate_mdx(
            cube=self,
            hierarchy_isin_conditions=hierarchy_isin_conditions,
            include_totals=include_totals,
            level_conditions=level_conditions,
            level_isin_conditions=level_isin_conditions,
            levels=levels,
            measures=measures,
            scenario=scenario,
        )

        # Remove this branch when https://github.com/activeviam/atoti/issues/1943 is done.
        if not measures:
            return (mdx, None)

        widget_conversion_details = WidgetConversionDetails(
            levels=[(level.dimension, level.hierarchy, level.name) for level in levels],
            mdx=mdx
            if include_totals
            else generate_mdx(
                cube=self,
                hierarchy_isin_conditions=hierarchy_isin_conditions,
                # Always use an MDX including totals because ActiveUI 5 only supports a subset of MDX.
                # See https://support.activeviam.com/jira/browse/UI-5036 and https://support.activeviam.com/jira/browse/UI-5268.
                include_totals=True,
                level_conditions=level_conditions,
                level_isin_conditions=level_isin_conditions,
                levels=levels,
                measures=measures,
                scenario=scenario,
            ),
            measures=[measure.name for measure in measures],
            source=session._get_widget_creation_source_code(),  # pylint: disable=protected-access
        )

        return mdx, widget_conversion_details

    @doc(_QUERY_DOC, args=_QUERY_ARGS_DOC)
    def query(
        self,
        *measures: QueryMeasure,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
        include_totals: bool = False,
        levels: Optional[Union[QueryLevel, Sequence[QueryLevel]]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
        **kwargs: Any,
    ) -> QueryResult:
        levels = [levels] if isinstance(levels, QueryLevel) else (levels or [])
        (
            mdx,
            widget_conversion_details,
        ) = self._generate_mdx_and_widget_conversion_details(
            condition=condition,
            include_totals=include_totals,
            levels=levels,
            measures=measures,
            scenario=ScenarioName(scenario),
            session=self._session,
        )
        query_result = self._session.query_mdx(
            mdx, keep_totals=include_totals, timeout=timeout, **kwargs
        )
        # pylint: disable=protected-access
        query_result._atoti_widget_conversion_details = widget_conversion_details
        # pylint: enable=protected-access

        return query_result


def _decombine_condition(
    condition: Optional[
        Union[
            LevelCondition,
            MultiCondition,
            LevelIsInCondition,
            HierarchyIsInCondition,
        ]
    ] = None,
) -> Tuple[
    Sequence[LevelCondition],
    Sequence[LevelIsInCondition],
    Sequence[HierarchyIsInCondition],
]:
    level_conditions: List[LevelCondition] = []
    level_isin_conditions: List[LevelIsInCondition] = []
    hierarchy_isin_conditions: List[HierarchyIsInCondition] = []

    if condition is not None:
        if isinstance(condition, LevelCondition):
            level_conditions.append(condition)
        elif isinstance(condition, LevelIsInCondition):
            level_isin_conditions.append(condition)
        elif isinstance(condition, HierarchyIsInCondition):
            hierarchy_isin_conditions.append(condition)
        elif isinstance(condition, MultiCondition):
            # pylint: disable=protected-access
            measure_conditions = condition._measure_conditions
            if measure_conditions:
                raise ValueError(
                    f"Multi-conditions with measures are not supported when querying cube:"
                    f" {measure_conditions}"
                )
            level_conditions += condition._level_conditions
            level_isin_conditions += condition._level_isin_conditions
            hierarchy_isin_conditions += condition._hierarchy_isin_condition
            # pylint: enable=protected-access
        else:
            raise TypeError(f"Unexpected type of query condition: f{type(condition)}")

    return level_conditions, level_isin_conditions, hierarchy_isin_conditions
