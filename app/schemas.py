
from pydantic import BaseModel, Field
from typing import Literal, Optional


class TaskCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=100
    )

    description: str = Field(
        default="",
        max_length=500
    )

    status: Literal[
        "pending",
        "in_progress",
        "completed"
    ] = "pending"


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    status: Optional[
        Literal[
            "pending",
            "in_progress",
            "completed"
        ]
    ] = None
