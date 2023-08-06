"""Reports of data loaded into stores.

Each store has a global :attr:`~atoti.store.Store.loading_report` made of several indiviual loading reports.

When an error occures while loading data, a warning is displayed.
These warnings can be disabled like this::

    import logging
    logging.getLogger("atoti.loading").setLevel("ERROR")
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from ._repr_utils import ReprJson, ReprJsonable

_LOGGER = logging.getLogger("atoti.loading")


@dataclass(frozen=True)
class LoadingReport(ReprJsonable):
    """Report about the loading of a single file or operation."""

    name: str
    """Name of the loaded file or operation."""
    source: str
    """Source used to load the data."""
    loaded: int
    """Number of loaded lines."""
    errors: int
    """Number of errors."""
    duration: int
    """Duration of the loading in milliseconds."""
    error_messages: List[str]
    """Messages of the errors."""

    def _repr_json_(self) -> ReprJson:
        data: Dict[str, Any] = {
            "loaded": self.loaded,
            "errors": self.errors,
            "source": self.source,
            "duration (ms)": self.duration,
        }
        if self.error_messages:
            data["error messages"] = self.error_messages
        return data, {"expanded": True, "root": self.name}


@dataclass(frozen=True)
class StoreReport(ReprJsonable):
    """Report about the data loaded into a store.

    It is made of several :class:`LoadingReport`.
    """

    store_name: str
    reports: List[LoadingReport]
    """Reports of indiviadual loading."""

    @property
    def total_loaded(self) -> int:
        """Total number of loaded rows."""
        return sum([r.loaded for r in self.reports])

    @property
    def total_errors(self) -> int:
        """Total number of errors."""
        return sum([r.errors for r in self.reports])

    @property
    def error_messages(self) -> List[str]:
        """Error messages."""
        return [message for r in self.reports for message in r.error_messages]

    def _repr_json_(self) -> ReprJson:
        data: Dict[str, Any] = {
            "total loaded": self.total_loaded,
            "total errors": self.total_errors,
        }
        messages = self.error_messages
        if messages:
            data["error messages"] = messages
        details = {r.name: r._repr_json_()[0] for r in self.reports}
        data["details per file"] = details
        return data, {"expanded": False, "root": "Store report"}


def _warn_new_errors(errors: Dict[str, int]):
    """Display a warning if there are new errors."""
    for store, error_count in errors.items():
        if error_count > 0:
            message = f"{error_count} error(s) occured while feeding the store {store}."
            message += " Check the store's loading_report for more details."
            _LOGGER.warning(message)
