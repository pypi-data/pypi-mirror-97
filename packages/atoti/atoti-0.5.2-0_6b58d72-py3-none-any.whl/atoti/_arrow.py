import json
from typing import Any, Mapping
from urllib.request import Request, urlopen

import pyarrow as pa

from .query.session import QuerySession

ATOTI_API_VERSION = "1"


def get_raw_query_endpoint(session: QuerySession) -> str:
    return f"{session._url}/atoti/rest/v{ATOTI_API_VERSION}/arrow/query"  # pylint: disable=protected-access


def run_raw_arrow_query(
    params: Mapping[str, Any],
    *,
    session: QuerySession,
) -> pa.Table:
    url = get_raw_query_endpoint(session)
    auth = session._auth(url) or {}  # pylint: disable=protected-access
    headers = {
        **auth,
        "Content-Type": "application/json",
    }
    req = Request(
        url, method="POST", headers=headers, data=json.dumps(params).encode("utf-8")
    )
    with urlopen(req) as response:  # nosec
        if response.status != 200:
            try:
                # Try to get the first error of the chain if it exists.
                error = RuntimeError(
                    f"Query failed: {json.loads(response)['error']['errorChain'][0]}"
                )
            except Exception:  # pylint: disable=broad-except
                error = RuntimeError(response.content)
            raise error
        record_batch_stream = pa.ipc.open_stream(response)
        return pa.Table.from_batches(
            record_batch_stream, schema=record_batch_stream.schema
        )
