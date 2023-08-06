from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, MutableMapping

from ._ipython_utils import ipython_key_completions_for_mapping
from .simulation import Simulation

if TYPE_CHECKING:
    from ._java_api import JavaApi


@dataclass
class Simulations(MutableMapping[str, Simulation]):
    """Manage the simulations."""

    _java_api: JavaApi = field(repr=False)
    _simulations: Dict[str, Simulation] = field(default_factory=dict)

    def __setitem__(self, key: str, value: Simulation) -> None:
        """Set the value for a given simulation."""
        self._simulations[key] = value

    def __getitem__(self, key: str) -> Simulation:
        """Get the simulation for a given key."""
        return self._simulations[key]

    def __delitem__(self, key: str) -> None:
        """Delete the simulation attached to the given key.

        This method both deletes the simlution from this dict and from the JVM by contacting the API.
        """
        try:
            value = self._simulations[key]
            self._java_api.delete_simulation(value)
            del self._simulations[key]
            self._java_api.refresh()
        except KeyError:
            raise KeyError(f"No simulation named {key}") from None

    def __iter__(self):
        """Return the iterator on simulations."""
        return iter(self._simulations)

    def __len__(self) -> int:
        """Return the number of simulations."""
        return len(self._simulations)

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self)
