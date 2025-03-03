from pydantic import BaseModel


class LanguageSchema(BaseModel):
    select_language: str
