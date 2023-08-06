from dataclasses import dataclass
from typing import Collection, Tuple

from .._version import VERSION

# Same naming scheme as our widgets.
# Keep in sync with convertQueryResultToWidgetMimeType in widgetMimeType.ts.
CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE = f"application/vnd.atoti.convert-query-result-to-widget.v{VERSION.split('.')[0]}+json"


@dataclass(frozen=True)
class WidgetConversionDetails:
    levels: Collection[Tuple[str, str, str]]
    mdx: str
    measures: Collection[str]
    source: str
