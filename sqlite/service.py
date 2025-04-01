from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from sqlite.database import SqliteSession
from sqlite.security import get_current_user


def get_db():
    db = SqliteSession()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
