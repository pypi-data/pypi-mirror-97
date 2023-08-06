from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class HttpRequest:
    """Info of an HTTP request."""

    url: str
    """URL on which the client request was made."""

    body: Any
    """Parsed JSON body of the request."""

    path_parameters: Mapping[str, str]
    """Mapping from the name of the path parameters to their value for this request."""
