from __future__ import annotations

from os import linesep
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Optional

import pandas as pd
from deepdiff import DeepDiff

from .config import SessionConfiguration, _parse_yaml_file_to_config


def diff_yaml_config_with_python_config(
    yaml_config: str, python_config: SessionConfiguration
) -> Optional[DeepDiff]:
    with NamedTemporaryFile(delete=False, mode="w", prefix="atoti-") as file:
        try:
            file.write(yaml_config)
            file.close()
            parsed_yaml_config = _parse_yaml_file_to_config(Path(file.name))
        finally:
            Path(file.name).unlink()

    # Return None when the diff is empty so that interactive examples can omit the output line when the configs are equal.
    return DeepDiff(parsed_yaml_config, python_config) or None


def monkey_patch_dataframe_repr_to_trim_trailing_whitespaces():
    """Used so that dataframes outputted in interactive examples match the expected output where trailing whitespaces have been trimmed by the IDE."""
    original_repr = pd.DataFrame.__repr__

    def patched_repr(*args: Any, **kwargs: Any) -> str:
        string = original_repr(*args, **kwargs)
        return linesep.join(line.rstrip() for line in string.splitlines())

    pd.DataFrame.__repr__ = patched_repr
