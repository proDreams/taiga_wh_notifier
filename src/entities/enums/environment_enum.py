from enum import Enum


class EnvironmentEnum(str, Enum):
    """
    Enum class to represent different environment configurations.

    :ivar DEV: String representation of the development environment.
    :type DEV: str
    :ivar TEST: String representation of the testing environment.
    :type TEST: str
    :ivar PROD: String representation of the production environment.
    :type PROD: str
    """

    DEV = "dev"
    TEST = "test"
    PROD = "prod"
