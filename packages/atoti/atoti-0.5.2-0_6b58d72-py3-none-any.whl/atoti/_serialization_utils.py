from abc import ABC, abstractmethod
from typing import Any, Mapping, Type, TypeVar

FromDictInheritedClass = TypeVar("FromDictInheritedClass")


# We do this by hand in order not to add a dependency and because the one we would like to use is not available on conda-forge anyway.
# See https://github.com/lidatong/dataclasses-json/issues/141.
# An advantage of doing it ourself is that we can provide stronger static typing.
# Indeed, with dataclasses-json, Pyright can't see that `Class.from_json` is of type `Class`.
class FromDict(ABC):
    """Base class for classes that can be built from a dict."""

    @classmethod
    @abstractmethod
    def _from_dict(
        cls: Type[FromDictInheritedClass], data: Mapping[str, Any]
    ) -> FromDictInheritedClass:
        """Take a dict an return an instance of the class.

        Args:
            cls: The class being built.
            data: The dict containing the class data.

        Returns:
            An instance of the class.

        """
