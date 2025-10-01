from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=150, description="The title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="The description of the task"
    )
    is_completed: bool = Field(..., description="The completion status of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="unique identifier of the task")
    created_date: datetime = Field(
        ..., description="The date and time the task was created"
    )
    updated_date: datetime = Field(
        ..., description="The date and time the task was updated"
    )
