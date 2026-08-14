from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Priority = Literal["Low", "Medium", "High"]


class TaskBase(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: Priority = "Medium"

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Task title cannot be empty"
            )

        return value


class TaskCreate(TaskBase):

    column_id: int


class TaskUpdate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: Priority = "Medium"

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Task title cannot be empty"
            )

        return value


class TaskMove(BaseModel):

    column_id: int


class TaskResponse(TaskBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    column_id: int
    created_at: datetime


class ColumnResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    position: int

    tasks: list[TaskResponse]


class BoardResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str

    columns: list[ColumnResponse]