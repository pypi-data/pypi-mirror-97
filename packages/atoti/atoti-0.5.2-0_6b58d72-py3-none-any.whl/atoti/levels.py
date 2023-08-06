from typing import Optional

from ._base._base_levels import BaseLevels, _LevelKey, _raise_multiple_levels_error
from .hierarchies import Hierarchies
from .level import Level


class Levels(BaseLevels[Level, Hierarchies]):
    """Flat representation of all the levels in the cube."""

    def __delitem__(self, key: _LevelKey):
        """Delete a level.

        Args:
            key: The name of the level to delete, or a ``(hierarchy_name, level_name)`` tuple.
        """
        if key not in self:
            raise KeyError(f"{key} is not an existing level.")
        lvl = self[key]
        hier = lvl._hierarchy
        if hier is None:
            raise ValueError("No hierarchy defined for level " + lvl.name)
        hier._java_api.drop_level(lvl)
        hier._java_api.refresh_pivot()

    def _find_level(
        self,
        dimension_name: Optional[str],
        hierarchy_name: Optional[str],
        level_name: str,
    ) -> Level:
        """Get a level from the hierarchy name and level name."""
        # pylint: disable=protected-access
        hierarchies = self._hierarchies._java_api.retrieve_hierarchy_for_level(
            self._hierarchies._cube, dimension_name, hierarchy_name, level_name
        )
        # pylint: enable=protected-access
        if len(hierarchies) > 1:
            _raise_multiple_levels_error(level_name, hierarchies)

        if len(hierarchies) == 0:
            raise KeyError(f"No level with name {level_name} found in cube.")

        hierarchy = hierarchies[0]

        return hierarchy.levels[level_name]
