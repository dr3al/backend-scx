from uuid import uuid4

from fastapi import Depends, UploadFile

from models import User
from repositories import UserRepository
from schemas.books import CreateBookSchema
from models.books import Book
from adapters.file_storage.base import FileStorageAdapter
from core.depends import get_file_storage
from core.exceptions import InvalidFileException, FileStorageException

ALLOWED_AVATAR_TYPES = {
    'image/jpeg': "jpg",
    'image/png': "png",
}
MAX_AVATAR_SIZE = 5 * 1024 * 1024 # 5mb


class UserService:
    def __init__(
            self,
            repository: UserRepository = Depends(),
            storage: FileStorageAdapter = Depends(get_file_storage)
    ):
        self.repository = repository
        self.storage = storage

    def upload_avatar(self, user: User, file: UploadFile) -> User:
        extension = ALLOWED_AVATAR_TYPES.get(file.content_type)
        if extension is None:
            raise InvalidFileException(
                "Неподдерживаемый тип файла",
                details={"allowed_types": list(ALLOWED_AVATAR_TYPES)},
            )

        data = file.file.read(MAX_AVATAR_SIZE + 1)
        if not data:
            raise InvalidFileException("Файл пустой")
        if len(data) > MAX_AVATAR_SIZE:
            raise InvalidFileException(
                "Файл слишком большой",
                details={"max_size_bytes": MAX_AVATAR_SIZE},
            )

        key = f"avatars/{user.id}/{uuid4().hex}.{extension}"
        avatar_url = self.storage.upload_file(key, data)

        return self.repository.update_avatar(user, avatar_url)