from typing import Optional

from .._base._base_levels import BaseLevels, _raise_multiple_levels_error
from .hierarchies import QueryHierarchies
from .level import QueryLevel


class QueryLevels(BaseLevels[QueryLevel, QueryHierarchies]):
    """Flat representation of all the levels in the cube."""

    def _find_level(
        self,
        dimension_name: Optional[str],
        hierarchy_name: Optional[str],
        level_name: str,
    ) -> QueryLevel:
        if dimension_name is None:
            if hierarchy_name is None:
                level = self._flatten()[level_name]
                if level is not None:
                    return level
                hierarchies = [
                    hierarchy
                    for ((_, lvl_name), hierarchy) in self._hierarchies.items()
                    if level_name == lvl_name
                ]
                return _raise_multiple_levels_error(level_name, hierarchies)

            return self._hierarchies[hierarchy_name][level_name]

        return self._hierarchies[(dimension_name, hierarchy_name)][level_name]  # type: ignore
