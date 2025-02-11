from dynaconf import Dynaconf

from src.core.Base.singleton import Singleton


class Configuration(Singleton):
    """
    Singleton implementation for managing application configuration.

    :ivar settings: Dynamic configuration object for loading and accessing settings from a YAML file.
    :type settings: Dynaconf
    """

    settings = Dynaconf(envvar_prefix=False, environments=True, settings_files=["config/settings.yaml"])
