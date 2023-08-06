from abc import abstractmethod
from typing import Any, Generic, Optional, cast

from .._ipython_utils import find_corresponding_top_level_variable_name
from .._plugins import MissingPluginError
from .._repr_utils import ReprJson, ReprJsonable
from ._base_cubes import _BaseCubes


class BaseSession(Generic[_BaseCubes], ReprJsonable):
    """Base class for session."""

    @property
    @abstractmethod
    def cubes(self) -> _BaseCubes:
        """Cubes of the session."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the session."""

    @property
    @abstractmethod
    def url(self) -> str:
        """URL of the session."""

    @property
    @abstractmethod
    def port(self) -> Optional[int]:
        """Port of the session."""

    def visualize(  # pylint: disable=no-self-use
        self, *args: Any, **kwargs: Any
    ) -> None:
        """atoti-jupyterlab is required."""
        raise MissingPluginError("jupyterlab")

    def _get_widget_creation_source_code(self) -> str:
        session_variable_name = find_corresponding_top_level_variable_name(self)

        if session_variable_name:
            return f"""{session_variable_name}.visualize()"""

        return f"""import atoti as tt\n\ntt.sessions["{self.name}"].visualize()"""

    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of a session."""
        cubes = self.cubes._repr_json_()[0]
        data = (
            {"Stores": cast(Any, self).stores._repr_json_()[0], "Cubes": cubes}
            if hasattr(self, "stores")
            else {"Cubes": cubes}
        )
        return (
            data,
            {"expanded": False, "root": self.name},
        )
