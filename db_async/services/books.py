from fastapi import Depends
from repositories.books import BookRepository
from schemas.books import CreateBookSchema
from models.books import Book


class BookService:
    def __init__(self, repository: BookRepository = Depends()):
        self.repository = repository

    async def create_book(self, book: CreateBookSchema) -> Book:
        create_result = await self.repository.create(book)

        output = book.model_dump()
        output.update({
            "id": create_result.id,
        })

        return output

    async def get_books_collection(self):
        pass

    async def get_book(self):
        pass

    async def edit_book(self):
        pass

    async def delete_book(self):
        pass
