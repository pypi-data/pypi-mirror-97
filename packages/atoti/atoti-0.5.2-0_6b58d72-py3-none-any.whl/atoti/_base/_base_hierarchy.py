from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Mapping, Tuple, TypeVar

from .._bitwise_operators_only import BitwiseOperatorsOnly, IdentityElement
from .._docs_utils import HIERARCHY_ISIN_DOC, doc
from .._hierarchy_isin_conditions import (
    HierarchyIsInCondition,
    create_condition_from_member_paths,
)
from .._repr_utils import ReprJson, ReprJsonable
from ._base_level import BaseLevel

_Levels = TypeVar("_Levels", bound=Mapping[str, BaseLevel])
_BaseHierarchy = TypeVar("_BaseHierarchy", bound="BaseHierarchy")


@dataclass(eq=False)
class BaseHierarchy(Generic[_Levels], ReprJsonable, BitwiseOperatorsOnly):
    """Hierarchy of a base cube."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the hierarchy."""

    @property
    @abstractmethod
    def dimension(self) -> str:
        """Name of the dimension of the hierarchy."""

    @property
    @abstractmethod
    def levels(self) -> _Levels:
        """Levels of the hierarchy."""

    @property
    @abstractmethod
    def slicing(self) -> bool:
        """Whether the hierarchy is slicing or not."""

    @property
    def _java_description(self) -> str:  # noqa: D401
        """Description for java."""
        return f"{self.name}@{self.dimension}"

    @doc(HIERARCHY_ISIN_DOC)
    def isin(self, *member_paths: Tuple[Any, ...]) -> HierarchyIsInCondition:
        return create_condition_from_member_paths(self, *member_paths)

    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of a hierarchy."""
        root = f"{self.name}{' (slicing)' if self.slicing else ''}"
        return (
            [level.name for level in self.levels.values()],
            {
                "root": root,
                "expanded": False,
            },
        )

    def _get_bool_alternative_message(self) -> str:  # pylint: disable=no-self-use
        return "For conditions on hierarchy members use the `isin` method."

    def _identity(self) -> Tuple[IdentityElement, ...]:
        return self.dimension, self.name
