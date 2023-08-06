import json
from typing import Any, Mapping, Optional, Union
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .._base._base_session import BaseSession
from .._docs_utils import doc
from ._cellset import Cellset, cellset_to_query_result
from ._context import Context
from ._discovery import Discovery
from ._discovery_utils import create_cubes_from_discovery
from .auth import Auth
from .cubes import QueryCubes
from .query_result import QueryResult

SUPPORTED_VERSIONS = ["5", "5.Z1", "4"]

_QUERY_MDX_ARGS_DOC = """Args:
            mdx: The MDX ``SELECT`` query to execute.
            keep_totals: Whether the returned DataFrame should contain, if they are present in the query result, the grand total and subtotals.
            timeout: The query timeout in seconds.
"""


_QUERY_MDX_DOC = f"""Execute an MDX query and return its result as a pandas DataFrame.

        {_QUERY_MDX_ARGS_DOC}
            keep_totals: Whether the resulting DataFrame should contain, if they are present in the query result, the grand total and subtotals.
                Totals can be useful but they make the DataFrame harder to work with since its index will have some empty values.

        Example:
            An MDX query that would be displayed as this pivot table:

            +---------------+-----------------+------------+------------+------------+------------+
            | Country       | Total Price.SUM | 2018-01-01 | 2019-01-01 | 2019-01-02 | 2019-01-05 |
            |               |                 +------------+------------+------------+------------+
            |               |                 | Price.SUM  | Price.SUM  | Price.SUM  | Price.SUM  |
            +---------------+-----------------+------------+------------+------------+------------+
            | Total Country |        2,280.00 |     840.00 |   1,860.00 |     810.00 |     770.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | China         |          760.00 |            |            |     410.00 |     350.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | France        |        1,800.00 |     480.00 |     500.00 |     400.00 |     420.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | India         |          760.00 |     360.00 |     400.00 |            |            |
            +---------------+-----------------+------------+------------+------------+------------+
            | UK            |          960.00 |            |     960.00 |            |            |
            +---------------+-----------------+------------+------------+------------+------------+

            will return this DataFrame:

            +------------+---------+-----------+
            | Date       | Country | Price.SUM |
            +============+=========+===========+
            | 2019-01-02 | China   | 410.0     |
            +------------+---------+-----------+
            | 2019-01-05 | China   | 350.0     |
            +------------+---------+-----------+
            | 2018-01-01 | France  | 480.0     |
            +------------+---------+-----------+
            | 2019-01-01 | France  | 500.0     |
            +------------+---------+-----------+
            | 2019-01-02 | France  | 400.0     |
            +------------+---------+-----------+
            | 2019-01-05 | France  | 420.0     |
            +------------+---------+-----------+
            | 2018-01-01 | India   | 360.0     |
            +------------+---------+-----------+
            | 2019-01-01 | India   | 400.0     |
            +------------+---------+-----------+
            | 2019-01-01 | UK      | 960.0     |
            +------------+---------+-----------+
"""


class QuerySession(BaseSession[QueryCubes]):
    """Used to query an existing session.

    Query sessions are considered immutable: the structure of their cubes is not expected to change.
    """

    def __init__(
        self, url: str, *, auth: Optional[Auth] = None, name: Optional[str] = None
    ):
        """Init.

        Args:
            url: The server base URL.
            auth: The authentication to use.
            name: The name to give to the session.
        """
        from .._plugins import get_active_plugins

        self._url = url
        self._name = name or url
        self._auth = auth or (lambda url: None)
        self._version = self._fetch_version()
        self._discovery = self._fetch_discovery()
        self._cubes = create_cubes_from_discovery(self._discovery, self)
        plugins = get_active_plugins()
        for plugin in plugins:
            plugin.init_query_session(self)

    @property
    def cubes(self) -> QueryCubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    def url(self) -> str:
        """URL of the session."""
        return self._url

    @property
    def port(self) -> Optional[int]:
        """Port of the session."""
        return urlparse(self.url).port

    def _generate_auth_headers(self) -> Mapping[str, str]:
        """Generate the authentication headers to use for this session."""
        return self._auth(self.url) or {}

    def _execute_json_request(self, url: str, *, body: Optional[Any] = None) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self._auth(url) or {})
        data = json.dumps(body).encode("utf8") if body else None
        # The user can send any URL, wrapping it in a request object makes it a bit safer
        request = Request(url, data=data, headers=headers)
        try:
            response = urlopen(request)  # nosec
            return json.load(response)
        except HTTPError as error:
            error_json = error.read()
            error_data = json.loads(error_json)
            raise RuntimeError("Request failed", error_data) from error

    def _fetch_versions(self) -> Any:
        url = f"{self._url}/versions/rest"
        return self._execute_json_request(url)

    def _fetch_version(self) -> str:
        response = self._fetch_versions()
        exposed_versions = [
            version["id"] for version in response["apis"]["pivot"]["versions"]
        ]
        try:
            return next(
                version for version in SUPPORTED_VERSIONS if version in exposed_versions
            )
        except Exception:
            raise RuntimeError(
                f"Exposed versions: {exposed_versions}"
                f" don't match supported ones: {SUPPORTED_VERSIONS}"
            ) from None

    def _fetch_discovery(self) -> Discovery:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/discovery"
        response = self._execute_json_request(url)
        return response["data"]

    def _query_mdx_to_cellset(self, mdx: str, *, context: Context) -> Cellset:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/query/mdx"
        body: Mapping[str, Union[str, Context]] = {"context": context, "mdx": mdx}
        response = self._execute_json_request(url, body=body)
        return response["data"]

    @doc(_QUERY_MDX_DOC)
    def query_mdx(
        self,
        mdx: str,
        *,
        keep_totals: bool = False,
        timeout: int = 30,
        **kwargs: Any,
    ) -> QueryResult:
        # We use kwargs to hide uncommon features from the public API.
        context: Context = kwargs.get("context", {})
        if timeout is not None:
            context = {**context, "queriesTimeLimit": timeout}
        cellset = self._query_mdx_to_cellset(mdx, context=context)
        query_result = cellset_to_query_result(
            cellset,
            context=context,
            discovery=self._discovery,
            get_level_data_types=kwargs.get("get_level_data_types"),
            keep_totals=keep_totals,
        )
        return query_result
