import inspect
from types import ModuleType
from typing import Any, Callable, Collection, Optional, Union

ContainerType = Union[type, ModuleType]


def _is_exported_element(
    element: Any, elem_module: Optional[ModuleType], exported_names: Collection[str]
) -> bool:
    try:
        # Make sure the element is part of atoti
        if not elem_module or not elem_module.__name__.startswith("atoti"):
            return False

        # If the element is private, it needs to be specifically exported.
        full_name = f"{elem_module.__name__}.{element.__name__}"
        if "._" in full_name:
            return element.__name__ in exported_names

        # All good.
        return True
    except AttributeError:
        return False


def walk_api(
    container: ContainerType,
    callback: Callable[[ContainerType, str], None],
    include_attribute: Optional[
        Callable[[ContainerType, str, Collection[str]], bool]
    ] = None,
):
    """Recursively explore the public API of the input container.

    Args:
        container: The container to explore.
        callback: The callback to invoke on all public functions.
            It takes the parent container of the exposed function and the function name as arguments.
        include_attribute: A function that returns whether the callback function should be invoked on the given attribute of the container.
            It takes the parent container, the attribute name and the collection of symbols explicitely exported by the container as inputs.
            If ``None``, this defaults to calling :func:`_is_exported_element` on the attribute.
    """
    # Retrieve the symbols explicitely exported by the container (if any).
    exported_names = getattr(container, "__all__", [])

    # Recursively iterate through all the attributes of the container to find public functions.
    for attr in dir(container):
        element = getattr(container, attr)

        # Make sure the element should be considered.
        if include_attribute:
            if not include_attribute(container, attr, exported_names):
                continue
        elif not _is_exported_element(
            element, inspect.getmodule(element), exported_names
        ):
            continue

        # Follow "container" types.
        if inspect.ismodule(element) or inspect.isclass(element):
            walk_api(element, callback)
            continue

        # Invoke the callback on functions.
        if inspect.isfunction(element) or inspect.ismethod(element):
            callback(container, attr)
            continue

        # What is this?
        raise RuntimeError(f"Unexpected element {element}")
