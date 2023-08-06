from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, TypeVar

_BaseMeasure = TypeVar("_BaseMeasure", bound="BaseMeasure")


@dataclass
class BaseMeasure:
    """Measure of a base cube."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the measure."""

    @property
    @abstractmethod
    def folder(self) -> Optional[str]:
        """Folder of the measure."""

    @property
    @abstractmethod
    def visible(self) -> bool:
        """Whether the measure is visible or not."""

    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Description of the measure."""

    @property
    @abstractmethod
    def formatter(self) -> Optional[str]:
        """Formatter of the measure."""
