# Description: A module to store the config data.
# because python_dotenv does not consider the environment variables set in the .env file. which are already set in the system.
# This module is used to store the config data in a class and access it using the class attributes.
import warnings
import tomllib
from singleton import SingleTon


class ProjConfigChangedWarning(UserWarning):
    """A warning to indicate that the config has been changed."""


class ProjConfigNameSpace:
    """A class to store the config data."""

    def __init__(self, config_name, **kwargs):
        self._name_ = config_name
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                setattr(self, k, ProjConfigNameSpace(k, **v))

    def get_name(self) -> str:
        """Get the name of the config."""
        return self._name_

    def __str__(self):
        output = f"\n{self._name_}:\n"
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            if isinstance(v, ProjConfigNameSpace):
                output += f"    {v.__str__()}\n"
            else:
                output += f"\t{v}\n"
        return output


class ProjConfig(SingleTon):
    """A class to store the config data."""

    _config_file = None
    _current_config = None
    _available_configs = []
    data = {}

    @property
    def config(self) -> ProjConfigNameSpace:
        """Get the current config."""
        return self._current_config

    @config.setter
    def config(self, config_name: str):
        """Set the current config."""
        if config_name not in self._available_configs:
            raise AttributeError(f"Config {config_name} not found.")
        if self.config:
            previous_warning_format = warnings.formatwarning
            ## custom warning message format to include the class name and the message
            warnings.formatwarning = lambda m, c, *_: f"\n{c.__name__}: {m}\n"
            warnings.warn(f"Config changed from {self.config.get_name()} to {config_name}.", ProjConfigChangedWarning)
            warnings.formatwarning = previous_warning_format
        self._current_config = ProjConfigNameSpace(config_name, **self.data[config_name])

    @property
    def config_file(self):
        """Get the config file name."""
        return self._config_file

    @config_file.setter
    def config_file(self, file_name: str):
        """Set the config file name."""
        self._config_file = file_name
        self._reload_config()

    def _reload_config(self):
        """Reload the config data."""
        with open(self._config_file, "rb") as file:
            self.data = tomllib.load(file)
            self._available_configs = list(self.data.keys())
            self._current_config = None

    @classmethod
    def load_from_toml(cls, file_path: str) -> "ProjConfig":
        """Load the config data from a toml file."""
        obj = cls()
        obj.config_file = file_path
        return obj


def get_config() -> ProjConfigNameSpace:
    """Get the config data. A helper function to get the config data. that can be used in other modules."""
    return ProjConfig().config


# Example usage
if __name__ == "__main__":
    FILE_NAME = "example_config.toml"
    cfg = ProjConfig.load_from_toml(FILE_NAME)
    cfg.config = "development"
    print(cfg.config)
    cfg.config = "production"
    print(cfg.config)
