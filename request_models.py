from pydantic import BaseModel, EmailStr, Field, StringConstraints
from typing_extensions import Annotated

Username = Annotated[
    str,
    StringConstraints(
        min_length=5,
        max_length=15,
        pattern=r"^[a-zA-Z0-9_]+$",  # Only letters, numbers, underscore
    ),
]


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: Username
    first_name: str
    last_name: str
    password: str
    role: str


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
