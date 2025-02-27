from enum import Enum


class KeyboardTypeEnum(str, Enum):
    """
    Enum class for representing different types of keyboards.

    :ivar INLINE: Represents an inline keyboard.
    :type INLINE: str
    :ivar REPLY: Represents a reply keyboard.
    :type REPLY: str
    """

    INLINE = "inline"
    REPLY = "reply"
