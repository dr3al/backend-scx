from enum import Enum

from fastapi import HTTPException, status

class ErrorCode(str, Enum):
    EMAIL_ALREADY_REGISTERED = "EMAIL_ALREADY_REGISTERED"
    USERNAME_ALREADY_REGISTERED = "USERNAME_ALREADY_REGISTERED"
    INCORRECT_CREDENTIALS = "INCORRECT_CREDENTIALS"
    FILE_STORAGE_ERROR = "FILE_STORAGE_ERROR"
    INVALID_FILE = "INVALID_FILE"

class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCode,
                 message: str, field=None, details=None, headers=None):
        super().__init__(
            status_code=status_code,
            headers=headers,
            detail={
                "ErrorCode": error_code.value,
                "ErrorMessage": message,
                "ErrorField": field,
                "ErrorContext": details
            })

class EmailAlreadyRegisteredException(AppException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.EMAIL_ALREADY_REGISTERED,
            message="Пользователь с таким email уже зарегистрирован.",
            details={
                "email": email
            }
        )

class FileStorageException(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code=ErrorCode.FILE_STORAGE_ERROR,
            message="Не удалось сохранить файл в хранилище.",
            details=details
        )

class InvalidFileException(AppException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.INVALID_FILE,
            message=message,
            field="file",
            details=details
        )
