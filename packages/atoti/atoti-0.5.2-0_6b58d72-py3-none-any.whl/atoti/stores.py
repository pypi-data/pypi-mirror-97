import logging
from pathlib import Path
from typing import Any, Dict

from ._ipython_utils import running_in_ipython
from ._java_api import JavaApi
from ._mappings import ImmutableMapping
from ._repr_utils import ReprJson, ReprJsonable
from .exceptions import AtotiJavaException
from .store import Store

_GRAPHVIZ_MESSAGE = (
    "Missing Graphviz library which is required to display the graph. "
    "It can be installed with Conda: `conda install graphviz` or by following the download instructions at https://www.graphviz.org/download/."
)


class Stores(ImmutableMapping[str, Store], ReprJsonable):
    """Manage the stores."""

    def __init__(self, java_api: JavaApi, mapping: Dict[str, Store]):
        """Init."""
        super().__init__(mapping)
        self._java_api = java_api

    def _repr_json_(self) -> ReprJson:
        return (
            dict(
                sorted(
                    {
                        store.name: store._repr_json_()[0] for store in self.values()
                    }.items()
                )
            ),
            {"expanded": False, "root": "Stores"},
        )

    @property
    def schema(self) -> Any:
        """Datastore schema as an SVG graph.

        Note:
            Graphviz is required to display the graph.
            It can be installed with Conda: ``conda install graphviz`` or by following the `download instructions <https://www.graphviz.org/download/>`_.

        Returns:
            An SVG image in IPython and a Path to the SVG file otherwise.
        """
        try:
            path = self._java_api.generate_datastore_schema_image()
            if running_in_ipython():
                from IPython.display import SVG

                return SVG(filename=path)
            return Path(path)
        except AtotiJavaException:
            logging.getLogger("atoti.stores").warning(_GRAPHVIZ_MESSAGE)
