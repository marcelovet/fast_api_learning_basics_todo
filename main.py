from fastapi import FastAPI

from routers import admin, auth, todo
from sqlite import models
from sqlite.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
