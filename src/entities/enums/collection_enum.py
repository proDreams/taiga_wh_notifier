from enum import Enum


class DBCollectionEnum(str, Enum):
    """
    Enum for defining common database collection names.

    :ivar PROJECT: Name of the project collection.
    :type PROJECT: str
    :ivar PROJECT_TYPE: Name of the project type collection.
    :type PROJECT_TYPE: str
    :ivar USERS: Name of the users collection.
    :type USERS: str
    """

    PROJECT = "project"
    PROJECT_TYPE = "project_type"
    USERS = "users"
