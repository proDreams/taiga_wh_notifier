from bson import ObjectId


def validate_object_id(value: str | ObjectId) -> str:
    """
    Converts an object ID to a string representation.

    :param value: The ObjectId or string to validate and convert.
    :type value: str | ObjectId
    :returns: A string representation of the object ID.
    :rtype: str
    :raises TypeError: If the input is neither a string nor an ObjectId instance.
    """
    return str(value)
