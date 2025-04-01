from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select
from starlette import status

from request_models import TodoRequest
from sqlite import models
from sqlite.service import db_dependency

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


@router.get("/")
async def read_all(db: db_dependency):
    return db.scalars(select(models.Todo)).all()  # type: ignore[attr-defined]


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, id: Annotated[int, Path(gt=0)]):
    todo = db.scalar(select(models.Todo).where(models.Todo.id == id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, request: TodoRequest):
    todo = models.Todo(**request.model_dump())
    db.add(todo)
    db.commit()


@router.put("/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, id: Annotated[int, Path(gt=0)], request: TodoRequest
):
    todo = db.scalar(select(models.Todo).where(models.Todo.id == id))
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
async def delete_todo(db: db_dependency, id: Annotated[int, Path(gt=0)]):
    todo = db.scalar(select(models.Todo).where(models.Todo.id == id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
