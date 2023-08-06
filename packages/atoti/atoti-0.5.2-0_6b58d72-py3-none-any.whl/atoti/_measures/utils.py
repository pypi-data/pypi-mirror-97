from __future__ import annotations

from typing import TYPE_CHECKING, Any, Collection, Mapping

from .._py4j_utils import as_java_object, to_java_object_array
from ..level import Level
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


def get_measure_name(java_api: JavaApi, measure: Measure, cube: Cube) -> str:
    """Get the name of the measure from either a measure or its name."""
    return measure._distil(java_api, cube, None)


def convert_level_in_description(levels: Collection[Level]) -> Collection[str]:
    """Get descriptions of the passed levels."""
    if any(not isinstance(level, Level) for level in levels):
        raise TypeError("All levels should be of type Level")
    return [lvl._java_description for lvl in levels]  # pylint: disable=protected-access


def convert_measure_args(
    java_api: JavaApi, cube: Cube, args: Collection[Any]
) -> Collection[Any]:
    """Convert a collection of arguments used for creating a measure in Java.

    The ``Measure`` arguments are replaced by their name, and other arguments are
    translated into Java-equivalent objects when necessary.
    """
    return [_convert_measure_arg(java_api, cube, a) for a in args]


def _convert_measure_arg(java_api: JavaApi, cube: Cube, arg: Any) -> Any:
    # Replace measures with their name.
    if isinstance(arg, Measure):
        return get_measure_name(java_api, arg, cube)

    # Recursively convert nested args.
    if isinstance(arg, tuple):
        return to_java_object_array(
            java_api.gateway, convert_measure_args(java_api, cube, arg)
        )
    if isinstance(arg, list):
        return convert_measure_args(java_api, cube, arg)
    if isinstance(arg, Mapping):
        return {
            _convert_measure_arg(java_api, cube, key): _convert_measure_arg(
                java_api, cube, value
            )
            for key, value in arg.items()
        }

    # Nothing smarter to do. Transform the argument to a java array.
    return as_java_object(java_api.gateway, arg)
