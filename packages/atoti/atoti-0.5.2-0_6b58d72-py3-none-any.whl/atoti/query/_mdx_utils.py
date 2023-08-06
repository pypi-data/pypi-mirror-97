from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Sequence, Tuple

from .._base._base_level import BaseLevel
from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._type_utils import BASE_SCENARIO, ScenarioName
from .hierarchy import QueryHierarchy
from .level import QueryLevel
from .measure import QueryMeasure

if TYPE_CHECKING:
    from .cube import QueryCube


def _escape(name: str) -> str:
    return name.replace("]", "]]")


def _generate_set(
    members: Sequence[str], *, single_element_short_syntax: bool = True
) -> str:
    if not members:
        raise ValueError("Empty sets are not supported.")

    if single_element_short_syntax and len(members) == 1:
        return next(iter(members))

    return f"""{{{", ".join(members)}}}"""


def _generate_columns_set(measures: Optional[Sequence[QueryMeasure]] = None) -> str:
    if not measures:
        return "[Measures].AllMembers"

    return _generate_set(
        [f"[Measures].[{_escape(measure.name)}]" for measure in measures],
        # ActiveUI 5 does not support it.
        # See https://support.activeviam.com/jira/browse/UI-5036.
        single_element_short_syntax=False,
    )


def _keep_only_deepest_levels(
    levels: Sequence[QueryLevel],
    *,
    cube: QueryCube,
) -> Mapping[QueryLevel, int]:
    hierarchy_to_max_level_depth: Dict[Tuple[str, str], int] = dict()

    for level in levels:
        hierarchy_coordinates = (level.dimension, level.hierarchy)
        current_max_level_depth = hierarchy_to_max_level_depth.get(
            hierarchy_coordinates, -1
        )
        level_depth = list(cube.hierarchies[hierarchy_coordinates].levels.keys()).index(
            level.name
        )

        if level_depth > current_max_level_depth:
            hierarchy_to_max_level_depth[hierarchy_coordinates] = level_depth

    return {
        list(cube.hierarchies[hierarchy_coordinates].levels.values())[depth]: depth
        for hierarchy_coordinates, depth in hierarchy_to_max_level_depth.items()
    }


def _generate_hierarchy_unique_name(dimension: str, hierarchy: str) -> str:
    return f"[{_escape(dimension)}].[{_escape(hierarchy)}]"


def _generate_level_set(
    level: QueryLevel, *, cube: QueryCube, include_totals: bool, level_depth: int
) -> str:
    hierarchy = cube.hierarchies[level.dimension, level.hierarchy]
    hierarchy_unique_name = _generate_hierarchy_unique_name(
        level.dimension, level.hierarchy
    )
    return (
        f"{hierarchy_unique_name}.[{_escape(level.name)}].Members"
        if hierarchy.slicing or not include_totals
        else f"Hierarchize(Descendants({{{hierarchy_unique_name}.[AllMember]}}, {level_depth + 1}, SELF_AND_BEFORE))"
    )


def _generate_rows_set(
    levels: Mapping[QueryLevel, int], *, cube: QueryCube, include_totals: bool
) -> str:
    if len(levels) == 1:
        level, level_depth = next(iter(levels.items()))
        return _generate_level_set(
            level, cube=cube, include_totals=include_totals, level_depth=level_depth
        )

    return f"""Crossjoin({", ".join(
        [
            _generate_level_set(level, cube=cube,include_totals=include_totals, level_depth=level_depth)
            for level, level_depth in levels.items()
        ]
    )})"""


def _ensure_condition_on_shallowest_level(level: BaseLevel, *, cube: QueryCube):
    if (
        next(iter(cube.hierarchies[level.dimension, level.hierarchy].levels))
        != level.name
    ):
        raise (
            ValueError(
                f"Only conditions based on the shallowest level of a hierarchy are supported but level ({level.dimension}, {level.hierarchy}, {level.name}) was given."
            )
        )


def _generate_hierarchy_coordinates_to_member_paths_from_conditions(
    *,
    cube: QueryCube,
    hierarchy_isin_conditions: Sequence[HierarchyIsInCondition],
    level_conditions: Sequence[LevelCondition],
    level_isin_conditions: Sequence[LevelIsInCondition],
) -> Mapping[Tuple[str, str], Sequence[Tuple[Any, ...]]]:
    hierarchy_coordinates_to_member_paths: Dict[
        Tuple[str, str], Sequence[Tuple[Any, ...]]
    ] = {}

    # pylint: disable=protected-access
    for level_condition in level_conditions:
        if level_condition._operation != "eq":
            raise (
                ValueError(
                    f"Only level conditions based on equality (==) are supported but operation {level_condition._operation} was given."
                )
            )

        _ensure_condition_on_shallowest_level(level_condition._level, cube=cube)

        hierarchy_coordinates_to_member_paths[
            level_condition._level.dimension, level_condition._level.hierarchy
        ] = [(level_condition._value,)]

    for condition in level_isin_conditions:
        _ensure_condition_on_shallowest_level(condition._level, cube=cube)

        hierarchy_coordinates_to_member_paths[
            condition._level.dimension, condition._level.hierarchy
        ] = [(member,) for member in condition._members]

    for condition in hierarchy_isin_conditions:
        hierarchy_coordinates_to_member_paths[
            condition._hierarchy.dimension, condition._hierarchy.name
        ] = [tuple(sub_dict.values()) for sub_dict in condition._members]
    # pylint: enable=protected-access

    return hierarchy_coordinates_to_member_paths


def _generate_member_unique_name(
    member_path: Sequence[str], *, hierarchy: QueryHierarchy
) -> str:
    parts = [_generate_hierarchy_unique_name(hierarchy.dimension, hierarchy.name)]

    for member in member_path:
        if not isinstance(member, str):
            raise (
                TypeError(
                    f"Only conditions against strings are supported but ({hierarchy.dimension}, {hierarchy.name}) was compared against {member} of type {type(member)}."
                )
            )

        parts.append(f"[{_escape(member)}]")

    return ".".join(parts)


def _generate_filter(
    *,
    hierarchy: QueryHierarchy,
    member_paths: Sequence[Tuple[Any, ...]],
) -> str:
    return _generate_set(
        [
            _generate_member_unique_name(member_path, hierarchy=hierarchy)
            for member_path in member_paths
        ]
    )


def _generate_filters(
    *,
    cube: QueryCube,
    hierarchy_coordinates_to_member_paths: Mapping[
        Tuple[str, str], Sequence[Tuple[Any, ...]]
    ],
    scenario: ScenarioName,
) -> Sequence[str]:
    filters = [
        _generate_filter(
            hierarchy=cube.hierarchies[
                hierarchy_coordinates[0], hierarchy_coordinates[1]
            ],
            member_paths=member_paths,
        )
        for hierarchy_coordinates, member_paths in hierarchy_coordinates_to_member_paths.items()
    ]

    if scenario != BASE_SCENARIO:
        filters.append(f"[Epoch].[Epoch].[{_escape(scenario)}]")

    return filters


def _generate_from_clause(
    cube: QueryCube,
    *,
    filters: Optional[Sequence[str]] = None,
) -> str:
    from_cube = f"FROM [{_escape(cube.name)}]"

    if not filters:
        return from_cube

    return f"FROM (SELECT {filters[-1]} ON COLUMNS {_generate_from_clause(cube, filters=filters[0:-1])})"


def generate_mdx(
    *,
    cube: QueryCube,
    hierarchy_isin_conditions: Sequence[HierarchyIsInCondition],
    include_totals: bool,
    levels: Sequence[QueryLevel],
    level_conditions: Sequence[LevelCondition],
    level_isin_conditions: Sequence[LevelIsInCondition],
    measures: Sequence[QueryMeasure],
    scenario: ScenarioName,
) -> str:
    """Return the corresponding MDX query.

    The value of the measures is given on all the members of the given levels.
    If no measure is specified then all the measures are returned.
    If no level is specified then the value at the top level is returned.
    """

    mdx = f"SELECT {_generate_columns_set(measures)} ON COLUMNS"

    deepest_levels = _keep_only_deepest_levels(levels, cube=cube)

    if deepest_levels:
        mdx = f"{mdx}, NON EMPTY {_generate_rows_set(deepest_levels, cube=cube, include_totals=include_totals)} ON ROWS"

    hierarchy_coordinates_to_member_paths = (
        _generate_hierarchy_coordinates_to_member_paths_from_conditions(
            cube=cube,
            hierarchy_isin_conditions=hierarchy_isin_conditions,
            level_conditions=level_conditions,
            level_isin_conditions=level_isin_conditions,
        )
    )

    filters = _generate_filters(
        cube=cube,
        hierarchy_coordinates_to_member_paths=hierarchy_coordinates_to_member_paths,
        scenario=scenario,
    )

    mdx = f"{mdx} {_generate_from_clause(cube, filters=filters)}"

    return mdx
