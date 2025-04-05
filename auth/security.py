from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from models.database_models import Users
from setup import settings as st

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__rounds=10,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
secret_key: str = st.SECRET_KEY  # type: ignore[assignment]
algorithm: str = st.ALGORITHM  # type: ignore[assignment]


def authenticate_user(username: str, password: str, db: Session):
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


def create_access_token(
    username: str,
    user_id: int,
    role: str,
    expires_delta: timedelta,
):
    encode = {"sub": username, "id": user_id, "role": role}
    expire = datetime.now(UTC) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, secret_key, algorithm=algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        user_role: str | None = payload.get("role")
        if username is None or user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username, "id": user_id, "user_role": user_role}
