from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, Mapping, Optional, Type, TypeVar, Union

from typing_extensions import Literal

from .._path_utils import PathLike, to_absolute_path
from ..sampling import DEFAULT_SAMPLING_MODE, SamplingMode
from ._auth import Auth
from ._auth_utils import parse_auth
from ._aws import AwsConfiguration
from ._azure import AzureConfiguration
from ._branding import Branding
from ._https import HttpsConfiguration
from ._jwt import JwtKeyPair
from ._role import Role
from ._utils import Configuration, defined_kwargs

DEFAULT_URL_PATTERN = "{protocol}://localhost:{port}"

SameSiteCookie = Literal["lax", "none", "strict"]

_T = TypeVar("_T")


def _get_or_fallback(main: _T, fallback: _T) -> _T:
    return main if main is not None else fallback


SubConfig = TypeVar("SubConfig", bound=Configuration)


def _pop_subconfig(
    field: str, config: Type[SubConfig], data: Dict[str, Any]
) -> Optional[SubConfig]:
    return config._from_dict(data.pop(field)) if field in data else None


@dataclass(frozen=True)
class SessionConfiguration(Configuration):
    """Configuration of the session."""

    authentication: Optional[Auth]
    aws: Optional[AwsConfiguration]
    azure: Optional[AzureConfiguration]
    branding: Optional[Branding]
    cache_cloud_files: Optional[bool]
    default_locale: Optional[str]
    extra_jars: Optional[Collection[str]]
    https: Optional[HttpsConfiguration]
    i18n_directory: Optional[str]
    inherit_global_config: bool
    java_args: Optional[Collection[str]]
    jwt_key_pair: Optional[JwtKeyPair]
    max_memory: Optional[str]
    metadata_db: Optional[str]
    port: Optional[int]
    roles: Optional[Collection[Role]]
    same_site: Optional[SameSiteCookie]
    sampling_mode: Optional[SamplingMode]
    url_pattern: Optional[str]

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        # Convert mapping to a dict to make it mutable with a pop method
        data_dict: Dict[str, Any] = dict(data)

        auth = (
            parse_auth(data_dict.pop("authentication"))
            if "authentication" in data_dict
            else None
        )

        aws = _pop_subconfig("aws", AwsConfiguration, data_dict)

        azure = _pop_subconfig("azure", AzureConfiguration, data_dict)

        branding = _pop_subconfig("branding", Branding, data_dict)

        https = _pop_subconfig("https", HttpsConfiguration, data_dict)

        i18n_directory = data_dict.pop("i18n_directory", None)

        jwt_key_pair = _pop_subconfig("jwt_key_pair", JwtKeyPair, data_dict)

        roles = (
            [Role._from_dict(role) for role in data_dict.pop("roles")]
            if "roles" in data_dict
            else None
        )

        sampling_mode = _pop_subconfig("sampling_mode", SamplingMode, data_dict)

        return create_config(
            **defined_kwargs(
                authentication=auth,
                aws=aws,
                azure=azure,
                branding=branding,
                https=https,
                i18n_directory=i18n_directory,
                jwt_key_pair=jwt_key_pair,
                roles=roles,
                sampling_mode=sampling_mode,
                **data_dict,
            ),
        )

    def _validate_before_completion(self):
        """Validate the merged config before applying the remaining default values."""
        if self.same_site:
            if not self.authentication:
                raise ValueError(
                    "same_site was needlessly configured since authentication is not set up"
                )

            if self.same_site == "none" and not (
                self.url_pattern and self.url_pattern.startswith("https://")
            ):
                raise ValueError(
                    "same_site was set to none which requires url_pattern to start with https://"
                )

    def _complete_with_default(self) -> SessionConfiguration:
        """Copy the config into a new one with the default values.

        These values should only be set if ``None`` is provided.
        They are not set in :func:`atoti.config.create_config` in order to support config inheritance.
        """
        self._validate_before_completion()

        return SessionConfiguration(
            authentication=self.authentication,
            aws=self.aws,
            azure=self.azure,
            branding=self.branding,
            cache_cloud_files=_get_or_fallback(self.cache_cloud_files, True),
            inherit_global_config=self.inherit_global_config,
            default_locale=self.default_locale,
            extra_jars=self.extra_jars,
            https=self.https,
            i18n_directory=self.i18n_directory,
            java_args=self.java_args,
            jwt_key_pair=self.jwt_key_pair,
            max_memory=self.max_memory,
            metadata_db=self.metadata_db,
            port=self.port,
            roles=self.roles,
            same_site=_get_or_fallback(self.same_site, "lax"),
            sampling_mode=_get_or_fallback(self.sampling_mode, DEFAULT_SAMPLING_MODE),
            url_pattern=_get_or_fallback(self.url_pattern, DEFAULT_URL_PATTERN),
        )


def merge_config(
    instance1: Optional[SessionConfiguration],
    instance2: Optional[SessionConfiguration],
) -> SessionConfiguration:
    """Merge two configurations. Second overrides the first one."""
    if instance1 is None:
        if instance2 is None:
            return create_config()
        return instance2
    if instance2 is None:
        return instance1
    return SessionConfiguration(
        authentication=_get_or_fallback(
            instance2.authentication, instance1.authentication
        ),
        aws=_get_or_fallback(instance2.aws, instance1.aws),
        azure=_get_or_fallback(instance2.azure, instance1.azure),
        branding=_get_or_fallback(instance2.branding, instance1.branding),
        cache_cloud_files=_get_or_fallback(
            instance2.cache_cloud_files, instance1.cache_cloud_files
        ),
        default_locale=_get_or_fallback(
            instance2.default_locale, instance1.default_locale
        ),
        extra_jars=_get_or_fallback(instance2.extra_jars, instance1.extra_jars),
        https=_get_or_fallback(instance2.https, instance1.https),
        i18n_directory=_get_or_fallback(
            instance2.i18n_directory, instance1.i18n_directory
        ),
        inherit_global_config=instance2.inherit_global_config,
        java_args=_get_or_fallback(instance2.java_args, instance1.java_args),
        jwt_key_pair=_get_or_fallback(instance2.jwt_key_pair, instance1.jwt_key_pair),
        max_memory=_get_or_fallback(instance2.max_memory, instance1.max_memory),
        metadata_db=_get_or_fallback(instance2.metadata_db, instance1.metadata_db),
        port=_get_or_fallback(instance2.port, instance1.port),
        roles=_get_or_fallback(instance2.roles, instance1.roles),
        same_site=_get_or_fallback(instance2.same_site, instance1.same_site),
        sampling_mode=_get_or_fallback(
            instance2.sampling_mode, instance1.sampling_mode
        ),
        url_pattern=_get_or_fallback(instance2.url_pattern, instance1.url_pattern),
    )


def create_config(
    *,
    authentication: Optional[Auth] = None,
    aws: Optional[AwsConfiguration] = None,
    azure: Optional[AzureConfiguration] = None,
    branding: Optional[Branding] = None,
    cache_cloud_files: Optional[bool] = None,
    default_locale: Optional[str] = None,
    extra_jars: Optional[Collection[PathLike]] = None,
    https: Optional[HttpsConfiguration] = None,
    i18n_directory: Optional[PathLike] = None,
    inherit_global_config: bool = True,
    java_args: Optional[Collection[str]] = None,
    jwt_key_pair: Optional[JwtKeyPair] = None,
    max_memory: Optional[str] = None,
    # Using `Union[Path, str]` instead of `PathLike` because the `str` can also represent a URL.
    metadata_db: Optional[Union[Path, str]] = None,
    port: Optional[int] = None,
    roles: Optional[Collection[Role]] = None,
    same_site: Optional[SameSiteCookie] = None,
    sampling_mode: Optional[SamplingMode] = None,
    url_pattern: Optional[str] = None,
) -> SessionConfiguration:
    """Create a session configuration.

    Note:
        Configuration inheritance is enabled by default.
        Pass ``inherit_global_config=False`` to prevent this configuration from being merged with the global one.

    Args:
        authentication:

            Note:
                This feature requires Atoti+.

            The authentication mechanism used by the server to configure which users are allowed to connect to the application and which roles they are granted.

        aws: The :mod:`atoti-aws <atoti_aws>` configuration.
        branding:

            Note:
                This feature requires Atoti+.

            The UI elements to change in the app to replace the atoti branding with another one.

        azure: The :mod:`atoti-azure <atoti_azure>` configuration.
        cache_cloud_files: Whether to cache loaded cloud files locally in the temp directory.
            Watched files will not be cached.

            Defaults to ``True``.

            .. doctest::
                :hide:

                >>> assert (
                ...     tt.config.create_config()
                ...     ._complete_with_default()
                ...     .cache_cloud_files
                ...     == True
                ... )

            Example:
                >>> python_config = tt.config.create_config(cache_cloud_files=False)
                >>> yaml_config = '''
                ... cache_cloud_files: false
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        default_locale:

            Note:
                This feature requires Atoti+.

            The default locale to use for internationalizing the session.

            Example:
                >>> python_config = tt.config.create_config(default_locale="fr-FR")
                >>> yaml_config = '''
                ... default_locale: fr-FR
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        extra_jars: A collection of JAR paths that will be added to the classpath of the Java process.

            Example:
                >>> python_config = tt.config.create_config(extra_jars=["../extra.jar"])
                >>> yaml_config = '''
                ... extra_jars:
                ...   - ../extra.jar
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        https:

            Note:
                This feature requires Atoti+.

            The certificate and its password used to enable HTTPS on the application.

        i18n_directory:

            Note:
                This feature requires Atoti+.

            The directory from which translation files will be loaded.

            It should contain a list of files named after their corresponding locale (e.g. ``en-US.json`` for US translations).
            The application will behave differently depending on how ``metadata_db`` is configured:

            * If ``metadata_db`` is a path to a file:

              - If a value is specified for ``i18n_directory``, those files will be uploaded to the local metadata DB, overriding any previously defined translations.
              - If no value is specified for ``i18n_directory``, the default translations for atoti will be uploaded to the local metadata DB.

            * If a remote metadata DB has been configured:

              - If a value is specified for ``i18n_directory``, this data will be pushed to the remote metadata DB, overriding any previously existing values.
              - If no value has been specified for ``i18n_directory`` and translations exist in the remote metadata DB, those values will be loaded into the session.
              - If no value has been specified for ``i18n_directory`` and no translations exist in the remote  metadata DB, the default translations for atoti will be uploaded to the remote metadata DB.

            Example:
                >>> python_config = tt.config.create_config(i18n_directory="../i18n")
                >>> yaml_config = '''
                ... i18n_directory: ../i18n
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        inherit_global_config: Whether this config should be merged with the default config if it exists.

            When working on multiple atoti projects, some configuration properties such as authentication or branding are often wanted to be shared.
            It is possible to do this sharing without repeating these properties by using configuration inheritance.

            To do so, the shared parts of the configuration can be declared in a global configuration file located at ``$ATOTI_HOME/config.yml`` where the ``$ATOTI_HOME`` environment variable defaults to ``$HOME/.atoti``.

            Example:
                >>> python_config = tt.config.create_config(inherit_global_config=False)
                >>> yaml_config = '''
                ... inherit_global_config: False
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        java_args: Collection of additional arguments to pass to the Java process (e.g. for optimization or debugging purposes).

            Example:
                >>> python_config = tt.config.create_config(
                ...     java_args=["-verbose:gc", "-Xms1g", "-XX:+UseG1GC"]
                ... )
                >>> yaml_config = '''
                ... java_args:
                ...   - -verbose:gc
                ...   - -Xms1g
                ...   - -XX:+UseG1GC
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        jwt_key_pair:

            Note:
                This feature requires Atoti+.

            The key pair to use for signing :abbr:`JWT (JSON Web Token)` s.

        max_memory: Max memory allocated to each session.

            atoti loads all the data in memory of the JVM. This option changes the ``-Xmx`` JVM parameter to increase the capacity of the application.

            The format is a string containing a number followed by a unit among ``G``, ``M`` and ``K``.

            Defaults to the JVM default memory which is 25% of the machine memory.

            Example:
                >>> python_config = tt.config.create_config(max_memory="64G")
                >>> yaml_config = '''
                ... max_memory: 64G
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        metadata_db: The description of the database where the session's metadata will be stored.

            Metadata is what is not part of the data sources, it includes content such as the dashboards saved by the users in the application.

            If a path to a file is given, it will be created if needed.

            Defaults to ``None`` meaning that the metadata is kept in memory and all its content is lost when the atoti session is closed.

            .. doctest::
                :hide:

                >>> assert (
                ...     tt.config.create_config()._complete_with_default().metadata_db
                ...     == None
                ... )

            Example:
                >>> python_config = tt.config.create_config(metadata_db="../metadata")
                >>> yaml_config = '''
                ... metadata_db: ../metadata
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        port: The port on which the session will be exposed.

            Defaults to a random available port.

            Example:
                >>> python_config = tt.config.create_config(port=8080)
                >>> yaml_config = '''
                ... port: 8080
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        roles:
            Note:
                This feature requires Atoti+.

            Roles restrict what users can see in a cube.
        same_site:

            Note:
                This feature requires Atoti+.

            The value to use for the `SameSite <https://web.dev/samesite-cookies-explained/>`_ attribute of the HTTP cookie sent by the session when ``authentication`` is configured.

            Setting it to ``none`` requires the session to be served in HTTPS so ``url_pattern`` must also be defined and start with ``https://``.

            Defaults to ``lax``.

            .. doctest::
                :hide:

                >>> assert (
                ...     tt.config.create_config()._complete_with_default().same_site
                ...     == "lax"
                ... )

            Example:
                >>> python_config = tt.config.create_config(same_site="strict")
                >>> yaml_config = '''
                ... same_site: strict
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        sampling_mode: The sampling mode used by default by the store when loading data.
            It is faster to build the data model when only part of the data is loaded.

            Modes are available in :mod:`atoti.sampling`.

            If not :data:`~atoti.sampling.FULL`, call :meth:`~atoti.session.Session.load_all_data` to load everything once the model definition is done.

            Defaults to ``atoti.sampling.first_lines(10000)``.

            .. doctest::
                :hide:

                >>> assert (
                ...     tt.config.create_config()._complete_with_default().sampling_mode
                ...     == tt.sampling.first_lines(10000)
                ... )

            Examples:

                * Load all data from the start:

                    >>> python_config = tt.config.create_config(
                    ...     sampling_mode=tt.sampling.FULL
                    ... )
                    >>> yaml_config = '''
                    ... sampling_mode: full
                    ... '''

                    .. doctest::
                        :hide:

                        >>> diff_yaml_config_with_python_config(
                        ...     yaml_config, python_config
                        ... )

                * Only load the first 1337 lines:

                    >>> python_config = tt.config.create_config(
                    ...     sampling_mode=tt.sampling.first_lines(1337)
                    ... )
                    >>> yaml_config = '''
                    ... sampling_mode:
                    ...   first_lines: 1337
                    ... '''

                    .. doctest::
                        :hide:

                        >>> diff_yaml_config_with_python_config(
                        ...     yaml_config, python_config
                        ... )

                * Only load the first 42 files:

                    >>> python_config = tt.config.create_config(
                    ...     sampling_mode=tt.sampling.first_files(42)
                    ... )
                    >>> yaml_config = '''
                    ... sampling_mode:
                    ...   first_files: 42
                    ... '''

                    .. doctest::
                        :hide:

                        >>> diff_yaml_config_with_python_config(
                        ...     yaml_config, python_config
                        ... )

        url_pattern: The pattern used to build the URL accessed through :attr:`atoti.session.Session.url`.
            The following placeholder replacements will be made:

                * ``{host}``: The address of the machine hosting the session.
                * ``{port}``: The port on which the session is exposed.
                * ``{protocol}``: ``http`` or ``https`` depending on whether the ``https`` option was defined or not.

            Defaults to ``{protocol}://localhost:{port}``.

            .. doctest::
                :hide:

                >>> # Check the documented default value.
                >>> assert (
                ...     tt.config.create_config()._complete_with_default().url_pattern
                ...     == "{protocol}://localhost:{port}"
                ... )

            Example:
                >>> python_config = tt.config.create_config(
                ...     url_pattern="http://{host}:{port}"
                ... )
                >>> yaml_config = '''
                ... url_pattern: http://{host}:{port}
                ... '''

                .. doctest::
                    :hide:

                    >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return SessionConfiguration(
        authentication=authentication,
        aws=aws,
        azure=azure,
        branding=branding,
        cache_cloud_files=cache_cloud_files,
        default_locale=default_locale,
        extra_jars=[to_absolute_path(jar) for jar in extra_jars]
        if extra_jars
        else None,
        https=https,
        i18n_directory=to_absolute_path(i18n_directory)
        if i18n_directory is not None
        else None,
        inherit_global_config=inherit_global_config,
        java_args=java_args,
        jwt_key_pair=jwt_key_pair,
        max_memory=max_memory,
        metadata_db=str(metadata_db.absolute())
        if isinstance(metadata_db, Path)
        else metadata_db,
        port=port,
        roles=roles,
        same_site=same_site,
        sampling_mode=sampling_mode,
        url_pattern=url_pattern,
    )
