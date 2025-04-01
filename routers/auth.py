from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from starlette import status

from request_models import CreateUserRequest, Token
from sqlite.models import Users
from sqlite.security import authenticate_user, create_access_token, pwd_context
from sqlite.service import db_dependency

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/users")
async def get_user(db: db_dependency):
    users = db.scalars(select(Users)).all()  # type: ignore[attr-defined]
    return users


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    create_user_model = Users(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=pwd_context.hash(request.password),
        is_active=True,
        role=request.role,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
