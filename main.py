from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from request_models import TodoRequest
from sqlite import models
from sqlite.database import SqliteSession, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SqliteSession()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: db_dependency):
    return db.scalars(select(models.Todo)).all()


@app.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, id: Annotated[int, Path(gt=0)]):
    todo = db.scalar(select(models.Todo).where(models.Todo.id == id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@app.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, request: TodoRequest):
    todo = models.Todo(**request.model_dump())
    db.add(todo)
    db.commit()


@app.put("/todo/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.delete("/todo/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, id: Annotated[int, Path(gt=0)]):
    todo = db.scalar(select(models.Todo).where(models.Todo.id == id))
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
