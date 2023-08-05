import lime_admin.plugins
from .schema import create_schema
import requests

class RuntimeConfig(lime_admin.plugins.AdminPlugin):
    """A class to represent the plugin in Lime Administration.

    An instance has access to a `lime_application.application.Application`
    object via `self.application`.

    """
    @property
    def name(self):
        """The name of the plugin

        Note:
            The name is used as the key when persisting the config and
            also as the key for the plugin itself
        """
        return 'limepkg_scrive'

    @property
    def title(self):
        """The title of the plugin
        """
        return 'Scrive eSigning'

    @property
    def version(self):
        """The version of the config

        Note:
            Should be incremented if
            the config format has changed. The version (if not None)
            is appended to the name when persisting the config
        """
        return None

    def get_config(self):
        """Function to retrieve a persisted config

        Note:
            If a config doesn't exist, then a default config should be
            persisted and then returned.

            If version has changed, then any existing config should be
            upgraded, persisted and then returned.

            There needs to be a really, really good reason for not returning
            a config at all.

        Returns:
            `dict`

        Raises:
            `lime_admin.plugins.NotFoundError` if the config doesn't exist.
        """
        defaultConfig = {
            "scriveHost": "https://lime.scrive.com",
            "scriveClientCredentialsIdentifier": "",
            "scriveClientCredentialsSecret": "",
            "scriveTokenCredentialsIdentifier": "",
            "scriveTokenCredentialsSecret": "",
            "limeHost": "",
            "limeApiKey": ""
        }
        try:
            config = super().get_config()
            if not "scriveHost" in config:
                config["scriveHost"] = defaultConfig["scriveHost"]
            if not "scriveClientCredentialsIdentifier" in config:
                config["scriveClientCredentialsIdentifier"] = defaultConfig["scriveClientCredentialsIdentifier"]
            if not "scriveClientCredentialsSecret" in config:
                config["scriveClientCredentialsSecret"] = defaultConfig["scriveClientCredentialsSecret"]
            if not "scriveTokenCredentialsIdentifier" in config:
                config["scriveTokenCredentialsIdentifier"] = defaultConfig["scriveTokenCredentialsIdentifier"]
            if not "scriveTokenCredentialsSecret" in config:
                config["scriveTokenCredentialsSecret"] = defaultConfig["scriveTokenCredentialsSecret"]
            if not "limeHost" in config:
                config["limeHost"] = defaultConfig["limeHost"]
            if not "limeApiKey" in config:
                config["limeApiKey"] = defaultConfig["limeApiKey"]
            return config
        except lime_admin.plugins.NotFoundError:
            return defaultConfig

    def get_schema(self):
        """Function to retrieve a schema for the config.

        Returns:
            :class:`marshmallow.Schema`
        """
        return create_schema(self.application)

    def set_config(self, config):
        """Function to persist a config.

        Note:
            The config should be validated before it's persisted.

        Args:
            config (dict): The config to be persisted.

        Raises:
            `lime_admin.plugins.ValueError` if the config is invalid.
        """
        scriveHost = config["scriveHost"]
        if scriveHost and not scriveHost.startswith( 'https://') and not scriveHost.startswith( 'http://localhost' ):
            raise lime_admin.plugins.ValueError("parameter 'scriveHost' needs to use 'https://' or 'http://localhost'")

        limeHost = config["limeHost"]
        if limeHost and not limeHost.startswith( 'https://') and not limeHost.startswith( 'http://localhost' ):
            raise lime_admin.plugins.ValueError("parameter 'limeHost' needs to use 'https://' or 'http://localhost'")

        try :
            url = config["scriveHost"] + '/api/config/'
            x = requests.post(url, data = config)
            if x.status_code == 200:
                super().set_config(config=config)
            else:
                error = x.json()["error"]
                raise lime_admin.plugins.ValueError(error if error else "unspecified error. please review your logs.")
        except requests.exceptions.ConnectionError:
            raise lime_admin.plugins.ValueError("could not contact 'scriveHost'.")



def register_config():
    """Function that is called by host when it's registering plugins

    Returns:
        :class:`Plugin`
    """
    return RuntimeConfig
