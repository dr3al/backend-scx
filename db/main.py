from fastapi import FastAPI

from api.books import router as books_router
from api.auth import router as auth_router
from api.users import router as users_router

from core.database import Base, engine
from core.handlers import register_exception_handlers

app = FastAPI()
app.include_router(books_router)
app.include_router(auth_router)

app.include_router(users_router)

register_exception_handlers(app)

Base.metadata.create_all(engine)