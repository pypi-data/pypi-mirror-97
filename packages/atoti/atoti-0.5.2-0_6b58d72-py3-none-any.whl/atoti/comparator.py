from dataclasses import dataclass
from typing import Any, Collection, Optional


@dataclass(frozen=True)
class Comparator:
    """Level comparator."""

    _name: str
    _first_members: Optional[Collection[Any]]


ASC = Comparator("ASC", None)
DESC = Comparator("DESC", None)


def first_members(*members: Any) -> Comparator:
    """Create a level comparator with the given first members.

    Example::

        atoti.comparator.first_members("gold", "silver", "bronze")

    """
    return Comparator("FIRST", list(members))
