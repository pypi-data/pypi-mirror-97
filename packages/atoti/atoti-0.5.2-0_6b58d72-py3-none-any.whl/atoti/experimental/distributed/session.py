from __future__ import annotations

from typing import Any

from ..._local_session import LocalSession
from ...config import SessionConfiguration
from .cube import DistributedCube
from .cubes import DistributedCubes


class DistributedSession(LocalSession[DistributedCubes]):
    """Holds a connection to the Java gateway."""

    def __init__(
        self,
        name: str,
        *,
        config: SessionConfiguration,
        **kwargs: Any,
    ):
        """Create the session and the Java gateway.

        Args:
            name: The name of the session.
            config: The configuration of the session.

        """
        super().__init__(name, config, True, **kwargs)
        self._cubes = DistributedCubes(self)

    def __enter__(self) -> DistributedSession:
        """Enter this session's context manager.

        Returns:
            self: to assign it to the "as" keyword.

        """
        return self

    @property
    def cubes(self) -> DistributedCubes:
        """Cubes of the session."""
        return self._cubes

    def create_cube(self, name: str) -> DistributedCube:
        """Create a distributed cube.

        Args:
            name: The name of the created cube.
        """
        self._java_api.create_distributed_cube(name)
        self._java_api.refresh(force_start=True, check_errors=False)
        return DistributedCube(self._java_api, name, self)
