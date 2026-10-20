from fastapi import FastAPI

from api.books import router as books_router
from api.auth import router as auth_router

from core.database import Base, engine
from models import User, Book

app = FastAPI()
app.include_router(books_router)
app.include_router(auth_router)

Base.metadata.create_all(engine)