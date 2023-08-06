from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping, Sequence, Tuple, Union

from ._base._base_hierarchies import _HierarchyKey
from ._local_hierarchies import LocalHierarchies
from .hierarchy import Hierarchy
from .level import Level
from .type import NULLABLE_OBJECT

if TYPE_CHECKING:
    from .cube import Cube
    from .store import Column

    LevelOrColumn = Union[Level, Column]


@dataclass(frozen=True)
class Hierarchies(LocalHierarchies[Hierarchy]):
    """Manage the hierarchies."""

    _cube: Cube = field(repr=False)

    def _get_underlying(self) -> Mapping[Tuple[str, str], Hierarchy]:
        return self._retrieve_hierarchies(self._java_api, self._cube)

    def __getitem__(self, key: _HierarchyKey) -> Hierarchy:
        (dim, hier) = self._convert_key(key)
        hierarchies = self._java_api.retrieve_hierarchy(self._cube, dim, hier)
        if len(hierarchies) == 0:
            raise KeyError(f"Unknown hierarchy: {key}")
        if len(hierarchies) == 1:
            return hierarchies[0]
        raise self._multiple_hierarchies_error(key, hierarchies)

    def __setitem__(
        self,
        key: _HierarchyKey,
        value: Union[Sequence[LevelOrColumn], Mapping[str, LevelOrColumn]],
    ):
        (dim, hier) = self._convert_key(key)
        if isinstance(value, Sequence):
            value = {column.name: column for column in value}
        elif not isinstance(value, Mapping):
            raise ValueError(
                f"Levels argument is expected to be a sequence or a mapping but is "
                f"{str(type(value).__name__)}"
            )
        # convert to Level
        levels: Mapping[str, Level] = {
            levelName: levelOrColumn
            if isinstance(levelOrColumn, Level)
            else Level(levelName, levelOrColumn.name, NULLABLE_OBJECT)
            for (levelName, levelOrColumn) in value.items()
        }

        # If the hierarchy is a single level hierarchy created from a store field, we
        # automatically put it in a dimension with the same name as the store
        # If the hierarchy is multilevel, the dimension is that of the store of the top most
        # level of the hierarchy.
        if dim is None:
            first_item = (
                value[0] if isinstance(value, Sequence) else list(value.values())[0]
            )
            if isinstance(first_item, Level):
                dim = first_item.dimension
            else:
                dim = first_item._store.name  # pylint: disable=protected-access

        hierarchies = self._java_api.retrieve_hierarchy(self._cube, dim, hier)
        if len(hierarchies) == 1:
            # Edit the existing hierarchy if there is one
            hierarchies[0].levels = levels
        elif len(hierarchies) == 0:
            # Create the new hierarchy
            self._java_api.create_or_update_hierarchy(self._cube, dim, hier, levels)
            self._java_api.refresh_pivot()
        else:
            raise self._multiple_hierarchies_error(key, hierarchies)

    def __delitem__(self, key: _HierarchyKey):
        try:
            self._java_api.drop_hierarchy(self._cube, self[key])
            self._java_api.refresh_pivot()
        except KeyError:
            raise KeyError(f"{key} is not an existing hierarchy.") from None
