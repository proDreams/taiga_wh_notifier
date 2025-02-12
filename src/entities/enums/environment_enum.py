from enum import Enum


class EnvironmentEnum(str, Enum):
    dev = "dev"
    test = "test"
    prod = "prod"
