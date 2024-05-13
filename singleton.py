"""A singleton metaclass to store only one instance of the class."""


class SingleTon(metaclass=type):
    """A singleton metaclass to store only one instance of the class."""

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]
