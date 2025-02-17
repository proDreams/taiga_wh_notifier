from pydantic import BaseModel, ConfigDict, field_validator

from src.core.settings import Configuration
from src.entities.schemas.base_data.base_schemas import IDSchema


class UserCreateSchema(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str

    @field_validator("language_code", mode="before")
    def validate_language_code(cls, value: object) -> object:
        if value not in Configuration.settings.ALLOWED_LANGUAGES:
            return Configuration.settings.DEFAULT_LANGUAGE
        return value

    model_config = ConfigDict(from_attributes=True)


class UserSchema(IDSchema, UserCreateSchema):
    pass
