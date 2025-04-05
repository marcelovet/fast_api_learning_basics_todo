from fastapi import FastAPI

from database.config import engine
from models import database_models
from routers import admin
from routers import auth
from routers import todo
from routers import users

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
async def healthy():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)
