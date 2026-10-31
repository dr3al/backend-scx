from abc import ABC, abstractmethod

class FileStorageAdapter(ABC):
    @abstractmethod
    async def upload_file(self, key: str, data: bytes):
        """Загрузка файла в хранилище"""
