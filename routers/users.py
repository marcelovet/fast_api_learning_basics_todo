from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from auth.security import authenticate_user, pwd_context
from models import database_models
from models.request_models import ChangePasswordRequest, ChangePhone
from service.dependencies import db_dependency, user_dependency

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
    return db.scalar(
        select(database_models.Users).where(database_models.Users.id == user.get("id"))
    )


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


@router.put("/change_phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency, db: db_dependency, request: ChangePhone
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    username: str = user.get("username", "")
    db_user = db.scalar(
        select(database_models.Users).where(database_models.Users.username == username)
    )
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.phone_number = request.phone_number
    db.commit()
