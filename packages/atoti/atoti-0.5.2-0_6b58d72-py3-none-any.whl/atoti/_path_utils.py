import os
from pathlib import Path
from typing import Union

from ._plugins import MissingPluginError, is_plugin_active

PathLike = Union[str, Path]
S3_IDENTIFIER = "s3://"
AZURE_BLOB_IDENTIFIER = ".blob.core.windows.net/"
GCP_IDENTIFIER = "gs://"


def _is_cloud_path(path: str) -> bool:
    """Check whether a path is a supported cloud path or not."""
    return path.startswith((S3_IDENTIFIER, GCP_IDENTIFIER)) or (
        AZURE_BLOB_IDENTIFIER in path
    )


def get_atoti_home() -> Path:
    """Get the path from $ATOTI_HOME env variable. If not defined, use $HOME/.atoti."""
    if "ATOTI_HOME" in os.environ:
        return Path(os.environ["ATOTI_HOME"])
    return Path.home() / ".atoti"


def stem_path(path: PathLike) -> str:
    """Return the final path component, without its suffix."""
    if isinstance(path, Path):
        return path.stem

    if isinstance(path, str):
        if _is_cloud_path(path):
            return path[path.rfind("/") + 1 :]
        return stem_path(Path(path))

    raise TypeError(
        f"Expected path to be of type str or pathlib.Path but was {type(path)}"
    )


def to_absolute_path(path: PathLike) -> str:
    """Transform the input path-like object into an absolute path.

    Args:
        path: A path-like object that points either to a local file or an AWS S3 file.
    """
    if isinstance(path, Path):
        return str(path.resolve())

    if isinstance(path, str):
        if _is_cloud_path(path):
            return path
        return str(Path(path).resolve())

    raise TypeError(
        f"Expected path to be of type str or pathlib.Path but was {type(path)}"
    )


def to_posix_path(path: PathLike) -> str:
    """Transform the input path-like object into a posix path.

    Args:
        path: A path-like object that points either to a local file or an AWS file.
    """
    if isinstance(path, Path):
        return str(path.as_posix())

    if isinstance(path, str):
        if path.startswith(S3_IDENTIFIER):
            if is_plugin_active("aws"):
                return path
            raise MissingPluginError("aws")
        if AZURE_BLOB_IDENTIFIER in path:
            if is_plugin_active("azure"):
                return path
            raise MissingPluginError("azure")
        if path.startswith(GCP_IDENTIFIER):
            if is_plugin_active("gcp"):
                return path
            raise MissingPluginError("gcp")

        # Do not resolve the path yet as it can contain a glob pattern that pathlib._WindowsFlavour does not support.
        # See also: https://github.com/python/cpython/pull/17
        return str(Path(path).as_posix())

    raise TypeError(
        f"Expected path to be of type str or pathlib.Path but was {type(path)}"
    )
