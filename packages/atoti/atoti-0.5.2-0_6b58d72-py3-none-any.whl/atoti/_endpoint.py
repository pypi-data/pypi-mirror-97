from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from ._py4j_utils import to_python_dict
from ._vendor.atotipy4j.java_collections import JavaMap
from .pyapi.http_request import HttpRequest
from .pyapi.user import User

if TYPE_CHECKING:
    from ._local_session import LocalSession

    CallbackEndpoint = Callable[[HttpRequest, User, LocalSession], str]


@dataclass
class PyApiEndpoint:
    """Session endpoint using a Python callback."""

    callback: CallbackEndpoint
    session: LocalSession
    name: str = "Python.PyApiEnpoint"

    def performRequest(  # pylint: disable=invalid-name
        self,
        url: str,
        body: str,
        user_name: str,
        roles: str,
        path_parameter_values: JavaMap,
    ) -> str:
        """Call when the associated route is requested.

        Args:
            url: The URL the user used for the query.
            body: String containing the request body.
                Only JSON is supported.
            user_name: Name of the user doing the query.
            roles: Roles of the user doing the query (string representing a set).
            path_parameter_values: Map from path parameter names to their values.
        """
        # convert the JavaMap to a python dict
        path_parameters = {
            str(key): str(value)
            for key, value in to_python_dict(
                path_parameter_values
            ).items()  # pylint: disable=unnecessary-comprehension
        }
        result_body = self.callback(
            HttpRequest(url, json.loads(body), path_parameters),
            User(user_name, roles[1 : len(roles) - 1].split(", ")),
            self.session,
        )
        return json.dumps(result_body)

    def toString(self) -> str:  # pylint: disable=invalid-name
        """To string."""
        return self.name

    class Java:
        """Code needed for Py4J callbacks."""

        implements = ["io.atoti.pyapi.PyApiEndpoint"]
