# Description: A module to store the config data.
# because python_dotenv does not consider the environment variables set in the .env file. which are already set in the system.
# This module is used to store the config data in a class and access it using the class attributes.
import typing as ty
import tomllib
from singleton import SingleTon


class ProjConfigNameSpace:
    """A class to store the config data.
    With config data as attributes of the class.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ProjConfig(SingleTon):
    """A class to store the config data."""

    config_file_name = ""

    def __init__(self):
        self._data = {}

    @property
    def data(self):
        """Get the config data."""
        return self._data

    @data.setter
    def data(self, data: ty.Dict[str, ty.Any]):
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def load(cls, file_path: str):
        """Load the config data from a toml file."""
        with open(file_path, "rb") as f:
            ProjConfig.config_file_name = file_path
            data = tomllib.load(f)
            config = cls()
            config.data = data
            return config


def load(file_path: str):
    """Load the config data."""
    ProjConfig.load(file_path)


def get(config_name: str, key: str) -> ty.Any:
    """Get the config value."""
    try:
        config = get_config(config_name)
        return getattr(config, key)
    except AttributeError as e:
        raise AttributeError(f"Config {config_name} not found.") from e


def get_config(config_name: str) -> ProjConfigNameSpace:
    """Get the config data."""
    try:
        config = getattr(ProjConfig(), config_name)
        return ProjConfigNameSpace(**config)
    except AttributeError as e:
        raise AttributeError(f"Config {config_name} not found.") from e


def get_config_file_name():
    """Get the config file name."""
    return ProjConfig.config_file_name


# Example usage
if __name__ == "__main__":
    FILE_NAME = "example_config.toml"
    load(FILE_NAME)
    prod_config = get_config("production")
    dev_config = get_config("development")
    print(prod_config)
    print(dev_config)
