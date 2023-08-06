import os
import re
from typing import Any

import yaml

ENV_MATCHER = re.compile(r".*\$\{\{\ ?env\.([^(}})^({{)^ ]+)\ ?\}\}.*")


def path_constructor(_: Any, node: Any):
    """Replace the environment variables."""
    value = str(node.value)
    match = ENV_MATCHER.match(value)
    while match is not None:
        var = match.groups()[0]
        value = re.sub(
            r"\$\{\{\ ?env\." + re.escape(var) + r"\ ?\}\}", os.environ[var], value
        )
        match = ENV_MATCHER.match(value)
    return value


class EnvVarLoader(yaml.SafeLoader):
    """Special loader replacing env variables."""


EnvVarLoader.add_implicit_resolver("!path", ENV_MATCHER, None)
EnvVarLoader.add_constructor("!path", path_constructor)
