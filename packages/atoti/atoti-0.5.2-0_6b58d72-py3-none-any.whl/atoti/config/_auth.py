from __future__ import annotations

from abc import abstractmethod

from ._utils import Configuration


class Auth(Configuration):
    """Abstract authentication."""

    @property
    @abstractmethod
    def _type(self) -> str:
        ...
