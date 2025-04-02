from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select
from starlette import status

from models import database_models
from models.request_models import TodoRequest
from service.dependencies import db_dependency, user_dependency

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    return db.scalars(  # type: ignore[attr-defined]
        select(database_models.Todo).where(
            database_models.Todo.owner_id == user.get("id")
        )
    ).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    todo = db.scalar(
        select(database_models.Todo).where(
            database_models.Todo.id == id,
            database_models.Todo.owner_id == user.get("id"),  # type: ignore[union-attr]
        )
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, request: TodoRequest):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    todo = database_models.Todo(**request.model_dump(), owner_id=user.get("id"))
    db.add(todo)
    db.commit()


@router.put("/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    id: Annotated[int, Path(gt=0)],
    request: TodoRequest,
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    todo = db.scalar(
        select(database_models.Todo).where(
            database_models.Todo.id == id,
            database_models.Todo.owner_id == user.get("id"),  # type: ignore[union-attr]
        )
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete
    db.commit()


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    todo = db.scalar(
        select(database_models.Todo).where(
            database_models.Todo.id == id,
            database_models.Todo.owner_id == user.get("id"),  # type: ignore[union-attr]
        )
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
