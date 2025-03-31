from fastapi import FastAPI

from sqlite import models
from sqlite.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
