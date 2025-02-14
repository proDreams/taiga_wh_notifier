from enum import Enum


class DBCollectionEnum(str, Enum):
    project = "project"
    project_type = "project_type"
    users = "users"
