from enum import Enum


class EnvironmentEnum(str, Enum):
    """
    Enum class to represent different environment configurations.

    :ivar dev: String representation of the development environment.
    :type dev: str
    :ivar test: String representation of the testing environment.
    :type test: str
    :ivar prod: String representation of the production environment.
    :type prod: str
    """

    dev = "dev"
    test = "test"
    prod = "prod"
