from enum import Enum


class ProjectsCommonMenuEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define types that can be performed in an editing context.

    """

    ADD = "add"
    EDIT = "ed"
