from __future__ import annotations

import logging
from abc import abstractmethod
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Mapping, Optional, Type, TypeVar, Union

from typing_extensions import Literal

from ._base._base_session import BaseSession
from ._docs_utils import doc
from ._endpoint import PyApiEndpoint
from ._java_api import JavaApi
from ._local_cubes import _LocalCubes
from ._path_utils import PathLike
from ._plugins import get_active_plugins
from ._query_plan import QueryAnalysis
from ._server_subprocess import ServerSubprocess
from ._transaction import Transaction
from ._type_utils import Port, typecheck
from ._vendor.atotipy4j.java_gateway import DEFAULT_PORT as _PY4J_DEFAULT_PORT
from .config import SessionConfiguration
from .exceptions import AtotiException, AtotiJavaException
from .logs import Logs
from .query.query_result import QueryResult
from .query.session import _QUERY_MDX_ARGS_DOC, _QUERY_MDX_DOC

if TYPE_CHECKING:
    from ._endpoint import CallbackEndpoint
    from .query.session import QuerySession

_CubeCreationMode = Literal[  # pylint: disable=invalid-name
    "auto", "manual", "no_measures"
]


def _resolve_metadata_db(metadata_db: str) -> str:
    if metadata_db.startswith("jdbc"):
        raise NotImplementedError("jdbc URLs are not yet supported.")

    # Remote URL don't need to be resolved
    if metadata_db.startswith("http://") or metadata_db.startswith("https://"):
        return metadata_db

    # Make sure the parent directory exists.
    path = Path(metadata_db)
    if path.exists() and not path.is_dir():
        raise ValueError(f"metadata_db is not a directory: {metadata_db}")
    path.mkdir(exist_ok=True)

    # Return the fully resolved path.
    return str(path.resolve())


_LocalSession = TypeVar("_LocalSession", bound="LocalSession")


@typecheck
class LocalSession(BaseSession[_LocalCubes]):
    """Local session class."""

    def __init__(
        self,
        name: str,
        config: SessionConfiguration,
        distributed: bool = False,
        **kwargs: Any,
    ):
        """Init."""
        self._name = name
        self._config = config

        self._create_subprocess_and_java_api(
            distributed,
            **kwargs,
        )

        try:
            self._configure_session()
        except AtotiJavaException as ave:
            # Raise an exception if the session configuration fails
            raise AtotiException(
                f"{ave.java_traceback}\n"
                f"An error occured while configuring the session.\n"
                f"The logs are availbe at {self.logs_path}"
            ) from None

        self._closed = False

    def _create_subprocess_and_java_api(
        self,
        distributed: bool,
        **kwargs: Any,
    ):
        py4j_java_port: Port
        if kwargs.get("detached_process", False):
            py4j_java_port = Port(_PY4J_DEFAULT_PORT)
            self._server_subprocess = None
            logging.getLogger("atoti.process").warning(
                "detached_process is True, expecting a running server with Py4J listening on port %d",
                py4j_java_port,
            )
        else:
            self._server_subprocess = ServerSubprocess(
                port=Port(self._config.port) if self._config.port else None,
                url_pattern=self._config.url_pattern,
                max_memory=self._config.max_memory,
                java_args=self._config.java_args,
                extra_jars=self._config.extra_jars,
                **kwargs,
            )
            py4j_java_port = self._server_subprocess.py4j_java_port
        self._java_api: JavaApi = JavaApi(
            py4j_java_port=py4j_java_port, distributed=distributed
        )

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    @abstractmethod
    def cubes(self) -> _LocalCubes:
        """Cubes of the session."""

    @property
    def closed(self) -> bool:
        """Return whether the session is closed or not."""
        return self._closed

    @property
    def port(self) -> int:
        """Port on which the session is exposed.

        Can be set in :class:`~atoti.config.SessionConfiguration`.
        """
        return self._java_api.get_session_port()

    @property
    def url(self) -> str:
        """Public URL of the session.

        Can be set in :class:`~atoti.config.SessionConfiguration`.
        """
        return self._java_api.get_session_url()

    @property
    def excel_url(self) -> str:
        """URL of the Excel endpoint.

        To connect to the session in Excel, create a new connection to an Analysis Services.
        Use this URL for the `server` field and choose to connect with "User Name and Password":

        * Without authentication, leave these fields blank.
        * With Basic authentication, fill them with your username and password.
        * Other authentication types (such as Auth0) are not supported by Excel.
        """
        return f"{self.url}/xmla"

    @property
    def logs_path(self) -> Path:
        """Path to the session logs file."""
        if not self._server_subprocess:
            raise NotImplementedError(
                "The logs path is not available when using a query server process"
            )
        return self._server_subprocess.logs_path

    def logs_tail(self, n: int = 20) -> Logs:
        """Return the n last lines of the logs or all the lines if ``n <= 0``."""
        with open(self.logs_path) as logs:
            lines = logs.readlines()
            last_lines = lines[-n:] if n > 0 else lines
            # Wrap in a Logs to display nicely.
            return Logs(last_lines)

    def _configure_session(self):
        """Configure the session."""
        # Configure the plugins first
        # pylint: disable=too-many-branches
        for plugin in get_active_plugins():
            plugin.init_session(self)

        if self._config is not None:
            self._java_api.configure_session(self._config)

        self._java_api.start_application()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit this session's context manager.

        Close the session.

        """
        self.close()

    def _clear(self):
        """Clear this session and free all the associated resources."""
        self._java_api.clear_session()

    def close(self) -> None:
        """Close this session and free all the associated resources."""
        self._java_api.shutdown()
        if self._server_subprocess:
            self.wait()
        self._closed = True

    def wait(self) -> None:
        """Wait for the underlying server subprocess to terminate.

        This will prevent the Python process to exit.
        """
        if self._server_subprocess is None:
            raise ValueError("Server subprocess is not defined")
        self._server_subprocess.wait()

    def _refresh(self):
        """Refresh the session."""
        self._java_api.refresh(force_start=False)

    def _generate_token(self) -> str:
        """Return a token that can be used to authenticate against the server."""
        return self._java_api.generate_jwt()

    def _setup_app_form(
        self,
        name: str,
        action: str,
        *,
        inputs: Optional[
            Mapping[str, Mapping[str, Union[bool, float, int, str]]]
        ] = None,
    ):
        """Set up a form to be used in the app served by the session.

        Example::

            session._setup_app_form(
                "Add city",
                f"{session.url}/atoti/pyapi/{route}",
                inputs={
                    "City": {"placeholder": "Name of the city", "required": True},
                    "Value": {
                        "placeholder": "Value for the city",
                        "required": True,
                        "type": "number",
                    },
                },
            )

        Args:
            name: The name of the form.
            action: The URL at which the form will be submitted.
            inputs: Map of input name to properties to set in the corresponding ``<input />`` HTML element.
                Some of the accepted properties are listed `here <https://github.com/DefinitelyTyped/DefinitelyTyped/blob/ed541cd6d5f5e12bf6447163a1d53c767ae3cd87/types/react/index.d.ts#L2083 >`_.
        """
        self._java_api.setup_app_form(name, action, inputs or {})

    def _open_transient_query_session(self) -> QuerySession:
        from .query.auth import Auth
        from .query.session import QuerySession

        headers = self._generate_auth_headers()
        auth: Optional[Auth] = (lambda _url: headers) if headers else None
        return QuerySession(f"http://localhost:{self.port}", auth=auth, name=self.name)

    @doc(_QUERY_MDX_DOC)
    def query_mdx(
        self, mdx: str, *, keep_totals: bool = False, timeout: int = 30
    ) -> QueryResult:
        return self._open_transient_query_session().query_mdx(
            mdx,
            get_level_data_types=lambda cube_name, levels_coordinates: self.cubes[  # pylint: disable=protected-access
                cube_name
            ]._get_level_data_types(
                levels_coordinates
            ),
            keep_totals=keep_totals,
            timeout=timeout,
        )

    @doc(args=_QUERY_MDX_ARGS_DOC)
    def explain_mdx_query(self, mdx: str, *, timeout: int = 30) -> QueryAnalysis:
        """Explain an MDX query.

        {args}
        """
        return self._java_api.analyse_mdx(mdx, timeout)

    def _generate_auth_headers(self) -> Mapping[str, str]:
        """Generate the authentication headers to use for this session."""
        return {"Authorization": f"Jwt {self._java_api.generate_jwt()}"}

    def start_transaction(self) -> Transaction:
        """Start a transaction to batch several store operations.

        * It is more efficient than doing each store operation one after the other.
        * It avoids possibly incorrect intermediate states (e.g. if loading some new data first requires to drop some existing one).

        .. note::
            Some operations are not allowed during a transaction:

            * Long-running operations such as :meth:`~atoti.store.Store.load_kafka` or :meth:`~atoti.store.Store.load_csv` where ``watch=True`` is used.
            * Operations changing the structure of the session's stores such as :meth:`~atoti.store.Store.join` or :meth:`~atoti.session.Session.read_parquet`.
            * Operations not related to data loading or dropping such as defining a new measure.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Berlin", 150.0),
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> store = session.read_pandas(
            ...     df, keys=["City"], store_name="start_transaction example"
            ... )
            >>> cube = session.create_cube(store)
            >>> extra_df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Singapore", 250.0),
            ...     ],
            ... )
            >>> with session.start_transaction():
            ...     store += ("New York", 100.0)
            ...     store.drop({"City": "Paris"})
            ...     store.load_pandas(extra_df)
            ...
            >>> store.head(10)
                       Price
            City
            Berlin     150.0
            London     240.0
            New York   100.0
            Singapore  250.0

        """
        return Transaction(self._java_api)

    def endpoint(
        self, route: str, *, method: Literal["POST", "GET", "PUT", "DELETE"] = "GET"
    ) -> Any:
        """Create a custom endpoint at ``f"{session.url}/atoti/pyapi/{route}"``.

        The decorated function must take three arguments with types :class:`~atoti.pyapi.user.User`, :class:`~atoti.pyapi.http_request.HttpRequest` and :class:`~atoti.session.Session` and return a response body as a Python data structure that can be converted to JSON.
        ``DELETE``, ``POST``, and ``PUT`` requests can have a body but it must be JSON.

        Path parameters can be configured by wrapping their name in curly braces in the route.

        Example::

            @session.endpoint("simple_get")
            def callback(request: HttpRequest, user: User, session: Session):
                return "something that will be in response.data"


            @session.endpoint(f"simple_post/{store_name}", method="POST")
            def callback(request: HttpRequest, user: User, session: Session):
                return request.path_parameters.store_name

        Args:
            route: The path suffix after ``/atoti/pyapi/``.
                For instance, if ``custom/search`` is passed, a request to ``/atoti/pyapi/custom/search?query=test#results`` will match.
                The route should not contain the query (``?``) or fragment (``#``).
            method: The HTTP method the request must be using to trigger this endpoint.
        """
        if route[0] == "/" or "?" in route or "#" in route:
            raise ValueError(
                f"Invalid route '{route}'. It should not start with '/' and not contain '?' or '#'."
            )

        def endpoint_decorator(func: CallbackEndpoint) -> Callable:
            self._java_api.create_endpoint(
                route,
                PyApiEndpoint(func, self),
                method,
                self.url,
            )
            return func

        return endpoint_decorator

    def export_translations_template(self, path: PathLike):
        """Export a template containing all translatable values in the session's cubes.

        Args:
            path: The path at which to write the template.
        """
        self._java_api.export_i18n_template(path)
