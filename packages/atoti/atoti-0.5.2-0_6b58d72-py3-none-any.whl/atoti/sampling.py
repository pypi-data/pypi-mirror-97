"""Sampling modes describe how data is loaded into stores.

atoti can handle very large volumes of data while still providing fast answers to queries.
However, loading a large amount of data during the modeling phase of the application is rarely a good idea because creating stores, joins, cubes, hierarchies and measures are all operations that take more time when there is more data.

atoti speeds up the sampling process by incoporating an automated sampling mechanism.

For instance, datasets can be automatically sampled on their :func:`first lines <first_lines>` while working on the model and then switched to the :attr:`full <FULL>` dataset when the project is ready to be shared with other users.

By reducing the amount of data, sampling is a way to have immediate feedback for each cell run in a notebook and keep the modeling phase as snappy as possible.

As a rule of thumb:

  * sampling is always recommended while building a project.
  * :meth:`~atoti.session.Session.load_all_data` should be called as late as possible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Mapping

from .config._utils import Configuration
from .config.parsing import ConfigParsingError

_LIMIT_FILES_NAME = "first_files"
_LIMIT_LINES_NAME = "first_lines"
_FULL_NAME = "full"


@dataclass(frozen=True)
class SamplingMode(Configuration):
    """Mode of source loading."""

    name: str
    """Name of the sampling mode."""

    parameters: List[Any]
    """Sampling parameters (number of lines, number of files, ...)."""

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        if data == _FULL_NAME:
            return _create_full()
        if len(data) > 1:
            raise ConfigParsingError("Only one sampling mode can be provided", data)
        if _LIMIT_FILES_NAME in data:
            return first_files(data[_LIMIT_FILES_NAME])
        if _LIMIT_LINES_NAME in data:
            return first_lines(data[_LIMIT_LINES_NAME])
        raise ConfigParsingError(
            f"Only {_LIMIT_FILES_NAME}, {_LIMIT_LINES_NAME} or {_FULL_NAME} sampling mode can be provided",
            data,
        )


def _get_warning_message(mode: SamplingMode) -> str:
    """Get the warning message corresponding to the given mode.

    Args:
        mode: The mode to get the message for.
    """
    if mode.name == _LIMIT_FILES_NAME:
        return f"there are more than {mode.parameters[0]} files to load."
    if mode.name == _LIMIT_LINES_NAME:
        return f"there are more than {mode.parameters[0]} lines in the files to load and the appended lines."
    # Default message. Should not be used but we nevers know.
    return "the sampling mode policy has breached."


def first_lines(limit: int) -> SamplingMode:
    """Mode to load only the first lines of the source.

    Args:
        limit: The maximum number of lines to read.
    """
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("Specify a positive integer value for the lines limit")
    return SamplingMode(_LIMIT_LINES_NAME, [limit])


def first_files(limit: int) -> SamplingMode:
    """Mode to load only the first files of the source.

    Args:
        limit: The maximum number of files to read.
    """
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("Specify a positive integer value for the files limit")
    return SamplingMode(_LIMIT_FILES_NAME, [limit])


def _create_full() -> SamplingMode:
    return SamplingMode(_FULL_NAME, [])


FULL = _create_full()
"""Load all the data in all the stores."""

DEFAULT_SAMPLING_MODE = first_lines(10000)
