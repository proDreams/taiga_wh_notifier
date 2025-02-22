from pydantic import BaseModel, ConfigDict, field_validator

from src.core.settings import Configuration
from src.entities.schemas.base_data.base_schemas import IDSchema


class UserCreateSchema(BaseModel):
    """
    Schema for user creation request.

    This schema is used to validate and structure the data required for creating a new user. It ensures that all necessary fields are present and correctly formatted.

    :ivar telegram_id: Unique identifier for the user on Telegram. Must be an integer.
    :type telegram_id: int
    :ivar first_name: The first name of the user. Must be a non-empty string.
    :type first_name: str
    :ivar last_name: The last name of the user. Can be None if not provided.
    :type last_name: str | None
    :ivar username: The username of the user. Can be None if not provided.
    :type username: str | None
    :ivar language_code: The ISO 639-1 language code for the user's preferred language. Must be one of the allowed languages or default to 'en' if not specified.
    :type language_code: str
    """

    telegram_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str
    is_admin: bool = False

    @field_validator("language_code", mode="before")
    def validate_language_code(cls, value: object) -> object:
        if value not in Configuration.settings.ALLOWED_LANGUAGES:
            return Configuration.settings.DEFAULT_LANGUAGE
        return value

    model_config = ConfigDict(from_attributes=True)


class UserSchema(IDSchema, UserCreateSchema):
    """
    Class representing the schema for user data.

    This class extends both IDSchema and UserCreateSchema to define a complete user schema that includes unique identifiers and creation details.

    :ivar id: The unique identifier for the user.
    :type id: str
    :ivar telegram_id: Unique identifier for the user on Telegram. Must be an integer.
    :type telegram_id: int
    :ivar first_name: The first name of the user. Must be a non-empty string.
    :type first_name: str
    :ivar last_name: The last name of the user. Can be None if not provided.
    :type last_name: str | None
    :ivar username: The username of the user. Can be None if not provided.
    :type username: str | None
    :ivar language_code: The ISO 639-1 language code for the user's preferred language. Must be one of the allowed languages or default to 'en' if not specified.
    :type language_code: str
    """

    pass
