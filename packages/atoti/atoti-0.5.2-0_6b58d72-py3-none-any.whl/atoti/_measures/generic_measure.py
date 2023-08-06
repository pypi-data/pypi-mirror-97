from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Tuple

from ..measure import Measure
from .utils import convert_measure_args

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


class GenericMeasure(Measure):
    """Generic implementation of a Measure."""

    _plugin_key: str
    _args: Tuple[Any, ...]

    def __init__(self, plugin_key: str, *args: Any):
        """Create the measure.

        Args:
            plugin_key: The plugin key of the Java implementation.
            args: The list of arguments used to create the measure.
                They are directly forwarded to the Java code, except for the ``Measure``
                arguments that are first created on the Java side and replaced by their name.
        """
        self._plugin_key = plugin_key
        self._args = args

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        return java_api.create_measure(
            cube,
            measure_name,
            self._plugin_key,
            *convert_measure_args(java_api, cube, self._args)
        )
