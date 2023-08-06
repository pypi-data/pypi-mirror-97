import os
import random
import re
import string
import time
from pathlib import Path
from subprocess import STDOUT, Popen  # nosec
from typing import Any, Collection, Optional, Tuple

from ._java_utils import DEFAULT_JAR_PATH, get_java_path
from ._path_utils import get_atoti_home
from ._plugins import get_active_plugins
from ._type_utils import Port

DEFAULT_HADOOP_PATH = Path(__file__).parent / "bin" / "hadoop-2.8.1-winutils"


def _create_session_directory() -> Path:
    """Create the directory that will contain the session files."""
    # Generate the directory name using a random string for uniqueness.
    random_string = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session_directory = get_atoti_home() / f"{str(int(time.time()))}_{random_string}"

    # Create the session directory and its known sub-folders.
    session_directory.mkdir(parents=True)
    _compute_log_directory(session_directory).mkdir()

    return session_directory


def _compute_log_directory(session_directory: Path) -> Path:
    """Return the path the the logs directory."""
    return session_directory / "logs"


def _get_hadoop_home() -> Optional[Path]:
    """Return the location of the HADOOP home directory."""
    if "HADOOP_HOME" in os.environ:
        return Path(os.environ["HADOOP_HOME"])
    if os.name == "nt":
        return DEFAULT_HADOOP_PATH
    return None


def get_plugin_jar_paths() -> Collection[str]:
    """Get the JAR paths of the available plugins."""
    return [
        str(plugin.get_jar_path())
        for plugin in get_active_plugins()
        if plugin.get_jar_path()
    ]


class ServerSubprocess:
    """A wrapper class to start and manage an atoti server from Python."""

    def __init__(
        self,
        port: Optional[Port] = None,
        url_pattern: Optional[str] = None,
        max_memory: Optional[str] = None,
        java_args: Optional[Collection[str]] = None,
        extra_jars: Optional[Collection[str]] = None,
        **kwargs: Any,
    ):
        """Create and start the subprocess.

        Args:
            port: The port on which the server will be exposed.
            url_pattern: The URL pattern for the server.
            max_memory: The max memory of the process.
            java_args: Arguments to pass to the Java process.
            extra_jars: Extra JARs to put in the classpath.
        """
        self.port = port
        self.url_pattern = url_pattern
        self.max_memory = max_memory
        self.java_args = java_args
        self.extra_jars = extra_jars or []
        self._session_directory = _create_session_directory()
        self._subprocess_log_file = (
            _compute_log_directory(self._session_directory) / "subprocess.log"
        )
        (self._process, self.py4j_java_port) = self._start(**kwargs)

    def wait(self) -> None:
        """Wait for the process to terminate.

        This will prevent the Python process to exit unless the Py4J gateway is closed since, in that case, the atoti server will stop itself.
        """
        self._process.wait()

    def _start(self, **kwargs: Any) -> Tuple[Popen, Port]:
        """Start the atoti server.

        Returns:
            A tuple containing the server process and the Py4J java port.
        """
        jar_from_kwargs = kwargs.get("jar_path")
        jar = Path(jar_from_kwargs) if jar_from_kwargs else DEFAULT_JAR_PATH

        if not jar.exists():
            raise FileNotFoundError(f"""Missing built-in atoti JAR at: "{jar}".""")

        process = self._create_subprocess(jar)

        # Wait for it to start
        try:
            java_port = self._await_start()
        except Exception as ex:
            process.kill()
            raise ex

        # We're done
        return (process, java_port)

    def _create_subprocess(self, jar: Path) -> Popen:
        """Create and start the actual subprocess.

        Args:
            jar: The path to the atoti JAR.

        Returns:
            The created process.
        """
        program_args = [
            str(get_java_path()),
            "-jar",
        ]

        program_args.append(f"-Dserver.session_directory={self._session_directory}")
        program_args.append("-Dserver.logging.disable_console_logging=true")

        if self.port:
            program_args.append(f"-Dserver.port={self.port}")

        if self.url_pattern:
            program_args.append(f"-Dserver.url_pattern={self.url_pattern}")

        if self.max_memory:
            program_args.append(f"-Xmx{self.max_memory}")

        if self.java_args:
            for arg in self.java_args:
                program_args.append(f"{arg}")

        hadoop_home = _get_hadoop_home()
        if hadoop_home:
            program_args.append(f"-Dhadoop.home.dir={str(hadoop_home.resolve())}")

        # Put JARs from user config or from plugins into loader path
        jars = [*self.extra_jars, *get_plugin_jar_paths()]
        if len(jars) > 0:
            program_args.append(f"-Dloader.path={','.join(jars)}")

        program_args.append(str(jar.absolute()))

        # Create and return the subprocess.
        # We allow the user to pass any argument to Java, even dangerous ones
        try:
            process = Popen(
                program_args,
                stderr=STDOUT,
                stdout=open(self._subprocess_log_file, "wt"),
            )  # nosec
        except Exception as ex:
            # Raise an exception containing the logs' path for the user
            raise Exception(
                f"Could not start the session. You can check the logs at {self._subprocess_log_file}",
            ) from ex

        return process

    def _await_start(self) -> Port:
        """Wait for the server to start and return the Py4J Java port."""
        period = 0.25
        timeout = 60
        attempt_count = round(timeout / period)
        # Wait for the process to start and log the Py4J port.
        for _attempt in range(1, attempt_count):  # pylint: disable=unused-variable
            # Look for the started line.
            try:
                for line in open(self._subprocess_log_file):
                    regex = "Py4J server started, listening for connections on port (?P<port>[0-9]+)"
                    match = re.search(regex, line.rstrip())
                    if match:
                        # Server should be ready.
                        return Port(int(match.group("port")))
            except FileNotFoundError:
                # The logs file has not yet been created.
                pass

            # The server is not ready yet.
            # Wait for a bit.
            time.sleep(period)

        # The inner loop did not return.
        # This means that the server could not be started correctly.
        raise Exception(
            "Could not start server. " + f"Check the logs: {self._subprocess_log_file}"
        )

    @property
    def logs_path(self) -> Path:
        """Path to the server log file."""
        return _compute_log_directory(self._session_directory) / "server.log"
