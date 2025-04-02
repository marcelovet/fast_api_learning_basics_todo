from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator
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
    password: Annotated[
        str,
        StringConstraints(min_length=8, max_length=64),
    ]
    phone_number: Annotated[
        str,
        StringConstraints(min_length=8, max_length=20),
    ]

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 64:
            raise ValueError("Password must be less than 64 characters")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        if not any(c in "@$!%*?&#" for c in v):
            raise ValueError("Password must contain a special character (@$!%*?&#)")
        return v


class ChangePasswordRequest(BaseModel):
    actual_password: Annotated[
        str,
        StringConstraints(min_length=8, max_length=64),
    ]
    new_password: Annotated[
        str,
        StringConstraints(min_length=8, max_length=64),
    ]

    @field_validator("actual_password", "new_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 64:
            raise ValueError("Password must be less than 64 characters")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        if not any(c in "@$!%*?&#" for c in v):
            raise ValueError("Password must contain a special character (@$!%*?&#)")
        return v


class ChangePhone(BaseModel):
    phone_number: Annotated[
        str,
        StringConstraints(min_length=8, max_length=20),
    ]


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
