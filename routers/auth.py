from fastapi import APIRouter

from request_models import CreateUserRequest
from sqlite.models import Users
from sqlite.service import db_dependency

router = APIRouter()


@router.post("/signup/")
async def create_user(db: db_dependency, request: CreateUserRequest):
    create_user_model = Users(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=request.password,
        is_active=True,
        role=request.role,
    )

    return create_user_model
