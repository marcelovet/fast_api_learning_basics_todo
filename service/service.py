from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.security import get_current_user
from database.config import SqliteSession


def get_db():
    db = SqliteSession()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
