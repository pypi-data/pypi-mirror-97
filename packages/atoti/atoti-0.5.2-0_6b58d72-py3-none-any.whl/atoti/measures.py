from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict

from ._local_measures import LocalMeasures
from .exceptions import AtotiJavaException
from .measure import Measure, MeasureLike, _convert_to_measure
from .named_measure import NamedMeasure

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .cube import Cube


def _validate_name(name: str):
    """Validate the measure name.

    Args:
        name: The name to check.
    """
    if "," in name:
        raise ValueError(f'Invalid measure name "{name}". "," are not allowed.')
    if name != name.strip():
        raise ValueError(
            f'Invalid measure name "{name}". Leading or trailing whitespaces are not allowed.'
        )
    if name.startswith("__hidden_"):
        raise ValueError(
            f'Invalid measure name "{name}". Name cannot start with "__hidden_".'
        )


@dataclass(init=False)
class Measures(LocalMeasures[NamedMeasure]):
    """Manage the measures."""

    def __init__(self, java_api: JavaApi, cube: Cube = field(repr=False)):
        super().__init__(java_api)
        self._cube = cube

    def _build_measure(
        self, name: str, description: JavaApi.MeasureDescription
    ) -> NamedMeasure:
        return NamedMeasure(
            name,
            description.underlying_type,
            self._cube,
            self._java_api,
            description.folder,
            description.formatter,
            description.visible,
            description.description,
        )

    def _get_underlying(self) -> Dict[str, NamedMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_full_measures(self._cube)
        return {
            name: self._build_measure(name, cube_measures[name])
            for name in cube_measures
        }

    def __getitem__(self, key: str) -> NamedMeasure:
        """Return the measure with the given name."""
        try:
            cube_measure = self._java_api.get_measure(self._cube, key)
            return self._build_measure(key, cube_measure)
        except AtotiJavaException:
            raise KeyError(f"No measure named {key}") from None

    def __setitem__(self, key: str, value: MeasureLike):
        """Publish the measure with the given name.

        If the input is not a Measure, its ``_to_measure`` method will be called.

        Args:
            key: The name of the measure to add.
            value: The measure to add.
        """
        _validate_name(key)

        if not isinstance(value, Measure):
            value = _convert_to_measure(value)

        try:
            value._distil(self._java_api, self._cube, key)
        except AttributeError as err:
            raise ValueError(f"Cannot create a measure from {value}") from err

        self._java_api.refresh_pivot()

    def __delitem__(self, key: str):
        """Delete a measure.

        Args:
            key: The name of the measure to delete.
        """
        found = self._java_api.delete_measure(self._cube, key)
        if not found:
            raise KeyError(f"{key} is not an existing measure.")
        self._java_api.refresh_pivot()
