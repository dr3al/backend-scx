from abc import ABC, abstractmethod

class FileStorageAdapter(ABC):
    @abstractmethod
    def upload_file(self, key: str, data: bytes):
        """Загрузка файла в хранилище"""
