from pathlib import Path
from tempfile import mkdtemp
from typing import Tuple

from ._path_utils import PathLike, to_posix_path


def _make_atoti_tempir() -> str:
    """Make an atoti temporary directory."""
    return mkdtemp(prefix="atoti-")


def _validate_csv_path(path: PathLike):
    """Check if the provided path meets our requirements.

    Args:
        path: the path to check.

    """
    if "*" in str(path):
        raise ValueError("The path could not be parsed correctly.")
    return path


def _split_csv_path_and_pattern(path: PathLike) -> Tuple[PathLike, str]:
    """Extract the glob pattern from the path if there is one.

    Args:
        path: The path to work on.

    Returns:
        The path and the extracted glob pattern.

    """
    # Start by searching for glob characters in the string
    path = to_posix_path(path)

    star_index = path.find("*")
    question_index = path.find("?")
    bracket_index = path.find("[") if path.find("]") > -1 else -1
    curly_index = path.find("{") if path.find("}") > -1 else -1

    first_index = min(
        i
        for i in [len(path) + 1, star_index, question_index, bracket_index, curly_index]
        if i > 0
    )

    if first_index == len(path) + 1:
        # We never found a match, return the path with the base pattern:
        return path, "glob:**.csv"

    # Search for the first / in the path before the beginning of the glob expression
    separators = [i for i, char in enumerate(path) if char == "/"]
    index = 0
    for i in sorted(separators):
        if i > first_index:
            break
        index = i
    return _validate_csv_path(Path(path[:index])), _validate_glob_pattern(path[index:])


def _validate_glob_pattern(pattern: str) -> str:
    """Check the pattern meets our requirements and modify it if necessary."""
    if ":" in pattern:
        split = pattern.split(":")
        if split[0] != "glob":
            raise ValueError("Only glob patterns are supported.")
        if split[1][0] == "/":
            # glob pattern doesn't need leading /
            split[1] = split[1][1:]
        pattern = ":".join(split)
        return pattern

    if pattern[0] == "/":
        # glob pattern doesn't need leading /
        pattern = pattern[1:]
    return f"glob:{pattern}"
