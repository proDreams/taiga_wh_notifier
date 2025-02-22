from enum import Enum


class DBCollectionEnum(str, Enum):
    PROJECT = "project"
    PROJECT_TYPE = "project_type"
    USERS = "users"
