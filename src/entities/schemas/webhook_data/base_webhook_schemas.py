from datetime import datetime

from pydantic import BaseModel


class BaseID(BaseModel):
    id: int


class BasePermalink(BaseModel):
    permalink: str


class BaseName(BaseModel):
    name: str


class TimeStamped(BaseModel):
    created_date: datetime | None = None
    modified_date: datetime | None = None


class BaseRequirement(BaseModel):
    client_requirement: bool | None = None
    team_requirement: bool | None = None
