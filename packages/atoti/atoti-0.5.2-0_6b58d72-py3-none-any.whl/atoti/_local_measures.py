from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, TypeVar

from atoti.query.measure import QueryMeasure

from ._base._base_measures import BaseMeasures
from ._mappings import DelegateMutableMapping
from .measure import MeasureLike
from .named_measure import NamedMeasure

if TYPE_CHECKING:
    from ._java_api import JavaApi

_Measure = TypeVar("_Measure", NamedMeasure, QueryMeasure)
_LocalMeasures = TypeVar("_LocalMeasures", bound="LocalMeasures")


@dataclass
class LocalMeasures(DelegateMutableMapping[str, _Measure], BaseMeasures[_Measure]):
    """Local measures class."""

    _java_api: JavaApi = field(repr=False)

    @abstractmethod
    def _get_underlying(self) -> Dict[str, _Measure]:
        """Fetch the measures from the JVM each time they are needed."""

    @abstractmethod
    def __getitem__(self, key: str) -> _Measure:
        """Return the measure with the given name."""

    @abstractmethod
    def __setitem__(self, key: str, value: MeasureLike):
        """Publish the measure with the given name.

        If the input is not a Measure, its ``_to_measure`` method will be called.

        Args:
            key: The name of the measure to add.
            value: The measure to add.
        """

    @abstractmethod
    def __delitem__(self, key: str):
        """Delete a measure.

        Args:
            key: The name of the measure to delete.
        """
