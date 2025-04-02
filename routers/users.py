from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from request_models import ChangePasswordRequest
from sqlite import models
from sqlite.security import authenticate_user, pwd_context
from sqlite.service import db_dependency, user_dependency

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    return db.scalar(select(models.Users).where(models.Users.id == user.get("id")))


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, request: ChangePasswordRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    username: str = user.get("username", "")
    db_user = authenticate_user(username, request.actual_password, db)
    db_user.hashed_password = pwd_context.hash(request.new_password)
    db.commit()
