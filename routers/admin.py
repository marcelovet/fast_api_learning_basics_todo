from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select
from starlette import status

from models import database_models
from service.dependencies import db_dependency, user_dependency

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/todo")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    return db.scalars(  # type: ignore[attr-defined]
        select(database_models.Todo)
    ).all()


@router.delete("/todo/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, id: Annotated[int, Path(gt=0)]
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    todo = db.scalar(select(database_models.Todo).where(database_models.Todo.id == id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
