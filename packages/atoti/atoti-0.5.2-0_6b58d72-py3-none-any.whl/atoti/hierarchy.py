from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Mapping

from ._base._base_hierarchy import BaseHierarchy
from .level import Level

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from ._local_cube import LocalCube
    from .hierarchies import Hierarchies
    from .levels import Levels
    from .measures import Measures


def _refresh_pivot_decorator(func: Callable[..., Any]) -> Callable:
    @wraps(func)
    def func_wrapper(self: Hierarchy, *args: Any, **kwArgs: Any) -> Any:
        # pylint: disable=protected-access
        func(self, *args, **kwArgs)
        self._java_api.refresh_pivot()
        # pylint: enable=protected-access

    return func_wrapper


@dataclass(eq=False)
class Hierarchy(BaseHierarchy[Mapping[str, Level]]):
    """Hierarchy of a Cube."""

    _name: str
    _levels: Mapping[str, Level]
    _dimension: str
    _slicing: bool
    _cube: LocalCube[Hierarchies, Levels, Measures] = field(repr=False)
    _java_api: JavaApi = field(repr=False)
    _visible: bool

    @property
    def levels(self) -> Mapping[str, Level]:
        return self._levels

    @property
    def dimension(self) -> str:
        return self._dimension

    @property
    def slicing(self) -> bool:
        return self._slicing

    @property
    def name(self) -> str:
        return self._name

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        return self._visible

    @levels.setter
    @_refresh_pivot_decorator
    def levels(self, value: Mapping[str, Level]):
        """Levels setter."""
        # pylint: disable=protected-access
        self._levels = value
        self._java_api.create_or_update_hierarchy(
            self._cube, self._dimension, self._name, self._levels
        )
        # pylint: enable=protected-access

    @dimension.setter
    @_refresh_pivot_decorator
    def dimension(self, value: str):
        """Dimension setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_coordinate(self._cube, self, value, self._name)
        self._dimension = value
        # pylint: enable=protected-access

    @slicing.setter
    @_refresh_pivot_decorator
    def slicing(self, value: bool):
        """Slicing setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_slicing(self, value)
        self._slicing = value
        # pylint: enable=protected-access

    @name.setter
    @_refresh_pivot_decorator
    def name(self, value: str):
        """Name setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_coordinate(
            self._cube, self, self._dimension, value
        )
        self._name = value
        # pylint: enable=protected-access

    @visible.setter
    @_refresh_pivot_decorator
    def visible(self, value: bool):
        """Visibility setter."""
        # pylint: disable=protected-access
        self._java_api.set_hierarchy_visibility(
            self._cube, self._dimension, self._name, value
        )
        self._visible = value
        # pylint: enable=protected-access
