from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy import select
from starlette import status

from request_models import CreateUserRequest
from sqlite.models import Users
from sqlite.security import pwd_context
from sqlite.service import db_dependency

SECRET_KEY = "a31b6458f79bfb8e08acad715e888376b61313f8b085a6b2c5e916b118f7f64b"
ALGORITHM = "HS256"

router = APIRouter()


def authenticate_user(username: str, password: str, db):
    user = db.scalar(select(Users).where(Users.username == username))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/users/")
async def get_user(db: db_dependency):
    users = db.scalars(select(Users)).all()
    return users


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return token
