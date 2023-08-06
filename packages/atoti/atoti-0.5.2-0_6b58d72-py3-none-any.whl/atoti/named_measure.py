from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

from ._base._base_measure import BaseMeasure
from .measure import Measure
from .type import DataType

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .cube import Cube


@dataclass(eq=False)
class NamedMeasure(Measure, BaseMeasure):
    """A named measure is a measure that has been published to the cube."""

    _name: str
    _data_type: DataType
    _cube: Cube = field(repr=False)
    _java_api: JavaApi = field(repr=False)
    _folder: Optional[str] = None
    _formatter: Optional[str] = None
    _visible: bool = True
    _description: Optional[str] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def folder(self) -> Optional[str]:
        """Folder of the measure.

        It can be changed by assigning a new value to the property (``None`` to clear it).
        """
        return self._folder

    @property
    def data_type(self) -> DataType:
        """Type of the measure members."""
        return self._data_type

    @folder.setter
    def folder(self, value: Optional[str]):
        """Folder setter."""
        self._folder = value
        self._java_api.set_measure_folder(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def formatter(self) -> Optional[str]:
        """Formatter of the measure.

        It can be changed by assigning a new value to the property (``None`` to clear it).

        Examples:
            * ``DOUBLE[0.00%]`` for percentages
            * ``DOUBLE[#,###]`` to remove decimals
            * ``DOUBLE[$#,##0.00]`` for dollars
            * ``DATE[yyyy-MM-dd HH:mm:ss]`` for datetimes

        The spec for the pattern between the ``DATE`` or ``DOUBLE``'s brackets is the one from `Microsoft Analysis Services <https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-format-string-contents?view=asallproducts-allversions>`_.
        The formatter only impacts how the measure is displayed, derived measures will still be computed from unformatted value.
        To round a measure, use :func:`atoti.math.round` instead.

        atoti provides an extra formatter for array measures:
            * ``ARRAY['|';1:3]`` this formatter allows you to choose the separator to use (``|`` in this example), and the slice of the array to display.
        """
        return self._formatter

    @formatter.setter
    def formatter(self, value: Optional[str]):
        """Formatter setter."""
        self._formatter = value
        self._java_api.set_measure_formatter(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def visible(self) -> bool:
        """Whether the measure is visible or not.

        It can be toggled by assigning a new boolean value to the property.
        """
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        """Visibility setter."""
        self._visible = value
        self._java_api.set_visible(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def description(self) -> Optional[str]:
        """Description of the measure."""
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        """Set the description of the measure."""
        self._description = value
        self._java_api.set_measure_description(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def _required_levels(self) -> List[str]:
        """Levels required by this measure."""
        return self._java_api.get_required_levels(self)

    def _do_distil(  # pylint: disable=no-self-use
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        raise ValueError("Cannot create a measure that already exists in the cube.")
