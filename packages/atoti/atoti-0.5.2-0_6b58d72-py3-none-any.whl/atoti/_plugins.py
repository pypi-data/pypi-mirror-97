from __future__ import annotations

import os
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any, Collection, Optional

if TYPE_CHECKING:
    from .query.session import QuerySession

_SUPPORTED_PLUGIN_CLASS_PREFIXES = {
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "jupyterlab": "JupyterLab",
    "kafka": "Kafka",
    "legacy-app": "LegacyApp",
    "sql": "SQL",
}

PLUGINS_ENVIRONMENT_VARIABLE = "ATOTI_PLUGINS"
"""Comma separated list of plugins to activate.

For instance: ``"aws,kafka"``.

If ``None``, all installed plugins will be activated.
"""


class Plugin(ABC):
    """Atoti Plugin."""

    @abstractmethod
    def static_init(self):
        """Init called once when the plugin module is imported.

        It can be used to monkey patch the public API to plug the real functions.
        """

    @abstractmethod
    def get_jar_path(self) -> Optional[Path]:
        """Return the path to the JAR."""

    @abstractmethod
    def init_session(self, session: Any):
        """Init called every time a session is created.

        It can be used to call some internal Java function to initialize the plugin.
        """

    @abstractmethod
    def init_query_session(self, query_session: QuerySession):
        """Init called every time a query session is created.

        It can be used to call Python functions to initialize the plugin.
        """


class MissingPluginError(ImportError):
    """Error thrown when a plugin is missing."""

    def __init__(self, plugin_key: str):
        """Init the error.

        This assumes that the plugin name is ``f"atoti-{plugin_key}"``.

        Args:
            plugin_key: The key of the plugin.
                It is also the name of the extra when installing the plugin with pip.
        """
        plugin_name = f"atoti-{plugin_key}"
        message = (
            f"The plugin {plugin_name} is missing, install it and try again."
            "\nThe plugin can be installed with pip or conda:"
            f"\n\t- pip install atoti[{plugin_key}]"
            f"\n\t- conda install {plugin_name}"
        )
        super().__init__(message)


def _find_active_plugins(
    keys_of_plugins_to_activate: Optional[Collection[str]] = None,
) -> Collection[Plugin]:
    """Find the active plugins."""
    plugins = []

    for plugin_key, plugin_class_prefix in _SUPPORTED_PLUGIN_CLASS_PREFIXES.items():
        if (
            keys_of_plugins_to_activate is None
            or plugin_key in keys_of_plugins_to_activate
        ):
            try:
                plugin_module = import_module(
                    f"atoti_{plugin_key.replace('-', '_')}._plugin"
                )
                plugin_class = getattr(plugin_module, f"{plugin_class_prefix}Plugin")
                plugins.append(plugin_class())
            except ImportError as error:
                if keys_of_plugins_to_activate is not None:
                    raise MissingPluginError(plugin_key) from error

    return plugins


_ACTIVE_PLUGINS: Optional[Collection[Plugin]] = None


def get_active_plugins() -> Collection[Plugin]:
    """Return all the active plugins."""
    global _ACTIVE_PLUGINS  # pylint: disable=global-statement

    if _ACTIVE_PLUGINS is None:
        _ACTIVE_PLUGINS = _find_active_plugins(
            os.environ[PLUGINS_ENVIRONMENT_VARIABLE].split(",")
            if PLUGINS_ENVIRONMENT_VARIABLE in os.environ
            else None
        )

    return _ACTIVE_PLUGINS


def is_plugin_active(plugin_key: str) -> bool:
    """Return whether the plugin is active or not."""
    plugin_class_name = f"{_SUPPORTED_PLUGIN_CLASS_PREFIXES[plugin_key]}Plugin"

    return next(
        (
            True
            for active_plugin in get_active_plugins()
            if active_plugin.__class__.__name__ == plugin_class_name
        ),
        False,
    )


def register_active_plugins():
    """Register all the active plugins."""
    for plugin in get_active_plugins():
        plugin.static_init()
