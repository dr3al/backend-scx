from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.exceptions import AppException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
            headers=exc.headers,
        )

    # @app.exception_handler(RequestValidationError)
    # def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    #     pass
