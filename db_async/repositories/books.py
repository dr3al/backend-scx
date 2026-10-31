from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from models.books import Book
from schemas.books import CreateBookSchema


class BookRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, book: CreateBookSchema) -> Book:
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        await self.db.commit()
        await self.db.refresh(db_book)

        return db_book

