from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Mapping, Optional, Type, Union

from ._mappings import DelegateMutableMapping
from ._repr_utils import ReprJson, ReprJsonable
from ._type_utils import typecheck
from .config import SessionConfiguration, _get_merged_config
from .experimental.distributed.session import DistributedSession
from .query.auth import Auth
from .query.session import QuerySession
from .session import Session

_Session = Union[Session, DistributedSession, QuerySession]


@dataclass(frozen=True)
class Sessions(DelegateMutableMapping[str, _Session], ReprJsonable):
    """Manage the sessions."""

    _sessions: Dict[str, _Session] = field(default_factory=dict)

    def _get_underlying(self) -> Mapping[str, _Session]:
        """Get the underlying mapping."""
        self._remove_closed_sessions()
        return self._sessions

    @typecheck
    def create_session(
        self,
        name: str = "Unnamed",
        *,
        config: Optional[Union[SessionConfiguration, Path, str]] = None,
        **kwargs: Any,
    ) -> Session:
        """Create a session.

        Args:
            name: The name of the session.
            config: The session configuration regrouping all the aspects of the session that might change dependending on where it is deployed.
                It can be passed either as:

                * A Python object created with :func:`atoti.config.create_config`.
                * A path to a YAML file, enabling the config to be changed without modifying the project's code.
                  Environment variables can be referenced (even recursively) in this file:

                  >>> yaml_config = '''
                  ... url_pattern: ${{ env.SOME_ENVIRONMENT_VARIABLE }}
                  ... '''

                  .. doctest::
                      :hide:

                      >>> import os
                      >>> os.environ["SOME_ENVIRONMENT_VARIABLE"] = "http://example.com"
                      >>> python_config = tt.config.create_config(
                      ...     url_pattern=os.environ["SOME_ENVIRONMENT_VARIABLE"]
                      ... )
                      >>> diff_yaml_config_with_python_config(
                      ...     yaml_config, python_config
                      ... )

        """
        merged_config = _get_merged_config(config)
        full_config = (
            merged_config._complete_with_default()  # pylint: disable=protected-access
        )
        self._clear_duplicate_sessions(name)
        session = Session(
            name,
            config=full_config,
            # We use kwargs to hide uncommon features from the public API.
            **kwargs,
        )
        self._sessions[name] = session
        return session

    @typecheck
    def _create_distributed_session(
        self,
        name: str,
        *,
        config: Optional[Union[SessionConfiguration, Path, str]] = None,
        **kwargs: Any,
    ) -> DistributedSession:
        """Create a distributed session.

        Args:
            name: The name of the session.
            config: The configuration of the session or the path to a configuration file.
        """
        merged_config = _get_merged_config(config)
        full_config = (
            merged_config._complete_with_default()  # pylint: disable=protected-access
        )
        self._clear_duplicate_sessions(name)
        session = DistributedSession(
            name,
            config=full_config,
            # We use kwargs to hide uncommon features from the public API.
            **kwargs,
        )
        self[name] = session
        return session

    @typecheck()
    def open_query_session(
        self, url: str, name: Optional[str] = None, *, auth: Optional[Auth] = None
    ) -> QuerySession:
        """Open an existing session to query it.

        This can be used to connect to:

          * Other sessions with another atoti process.
          * ActivePivot cubes built with a classic Java project, if version >= 5.7.0.

        Args:
            url: The server base URL.
                ``{url}/versions/rest`` is expected to exist.
            name: The name to give to the session.
                Defaults to ``url``.
            auth: The authentication to use.
                It is a function taking the request URL and returning a dictionary of HTTP headers
                to include in the request.

                Example::

                    auth=lambda url: {"Authorization": f"Bearer {token}"}

                There are some built-in helpers: :func:`atoti.query.create_basic_authentication` and :func:`atoti.query.create_token_authentication`.
        """
        name = name or url
        self._clear_duplicate_sessions(name)
        query_session = QuerySession(url, auth=auth, name=name)
        self[name] = query_session
        return query_session

    def _clear_duplicate_sessions(self, name: str):
        if name in self._sessions:
            logging.getLogger("atoti.session").warning(
                """Deleting existing "%s" session to create the new one.""", name
            )
            del self[name]

    def __enter__(self) -> Sessions:
        """Enter this sessions manager's context manager.

        Returns:
            Ourself to assign it to the "as" keyword.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit this sessions' context manager.

        Close all the managed sessions.
        """
        self.close()

    def close(self):
        """Close all the managed sessions."""
        for session in self._sessions.values():
            if isinstance(session, Session):
                session.close()

    def _remove_closed_sessions(self) -> None:
        sessions_to_remove = [
            session
            for session in self._sessions.values()
            if isinstance(session, Session) and session.closed
        ]
        for session in sessions_to_remove:
            del self._sessions[session.name]

    def __setitem__(self, key: str, value: _Session) -> None:
        """Add a session."""
        self._remove_closed_sessions()
        if key in self._sessions:
            del self[key]
        self._sessions[key] = value

    def __getitem__(self, key: str) -> _Session:
        """Get a session."""
        self._remove_closed_sessions()
        return self._sessions[key]

    def __delitem__(self, key: str) -> None:
        """Remove a session.

        This method also stops the Java session, destroying all Java objects attached to it.
        """
        self._remove_closed_sessions()
        if key in self._sessions:
            session = self._sessions[key]
            if isinstance(session, Session):
                session.close()
            del self._sessions[key]

    def _repr_json_(self) -> ReprJson:
        return (
            {name: session._repr_json_()[0] for name, session in sorted(self.items())},
            {"root": "Sessions", "expanded": False},
        )
