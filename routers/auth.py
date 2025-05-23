from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth.security import authenticate_user
from auth.security import create_access_token
from auth.security import pwd_context
from models.database_models import Users
from models.request_models import CreateUserRequest
from models.request_models import Token
from service.dependencies import db_dependency

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    create_user_model = Users(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=pwd_context.hash(request.password),
        is_active=True,
        role="user",
        phone_number=request.phone_number,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20),
    )
    return {"access_token": token, "token_type": "bearer"}
