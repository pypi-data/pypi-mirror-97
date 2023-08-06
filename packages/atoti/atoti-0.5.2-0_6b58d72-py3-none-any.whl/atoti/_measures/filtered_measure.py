from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Collection, Optional, Sequence

from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._py4j_utils import as_java_object, to_java_object_list
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class WhereMeasure(Measure):
    """A measure that returns the value of other measures based on conditions."""

    _true_measure: Measure
    _false_measure: Optional[Measure]
    _conditions: Sequence[Measure]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = self._true_measure._distil(java_api, cube, None)
        underlying_else_name = (
            self._false_measure._distil(java_api, cube, None)
            if self._false_measure is not None
            else None
        )
        conditions_names = [
            condition._distil(java_api, cube, None) for condition in self._conditions
        ]
        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "WHERE",
            underlying_name,
            underlying_else_name,
            conditions_names,
        )
        return distilled_name


@dataclass(eq=False)
class LevelValueFilteredMeasure(Measure):
    """A measure on a part of the cube filtered on a level value."""

    _underlying_measure: Measure
    _level_conditions: Optional[Collection[LevelCondition]] = field(
        default_factory=tuple
    )
    _level_isin_conditions: Optional[Collection[LevelIsInCondition]] = field(
        default_factory=tuple
    )
    _hierarchy_isin_conditions: Optional[Collection[HierarchyIsInCondition]] = field(
        default_factory=tuple
    )

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        from ..level import Level

        # Distill the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)

        # pylint: disable=protected-access
        conditions = []
        if self._level_conditions:
            conditions += [
                {
                    "level": condition._level,
                    "type": "other",
                    "operation": condition._operation,
                    "value": condition._value.name,
                }
                if isinstance(condition._value, Level)
                else {
                    "level": condition._level,
                    "type": "literal",
                    "operation": condition._operation,
                    "value": as_java_object(java_api.gateway, condition._value),
                }
                for condition in self._level_conditions
            ]
        if self._level_isin_conditions:
            conditions += [
                {
                    "level": condition._level,
                    "type": "literal",
                    "operation": condition._operation,
                    "value": to_java_object_list(java_api.gateway, condition._members),
                }
                for condition in self._level_isin_conditions
            ]

        if self._hierarchy_isin_conditions:
            conditions += [
                {
                    "level": list(list(condition._members)[0].keys())[0],
                    "type": "literal",
                    "operation": condition._operation,
                    "value": condition._members,
                }
                for condition in self._hierarchy_isin_conditions
            ]
        # pylint: enable=protected-access

        # Create the filtered measure and return its name.
        distilled_name = java_api.create_measure(
            cube, measure_name, "FILTER", underlying_name, conditions
        )
        return distilled_name
