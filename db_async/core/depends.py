import jwt
from datetime import datetime, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from adapters.file_storage.base import FileStorageAdapter
from repositories.users import UserRepository
from adapters.file_storage.s3 import S3FileStorageAdapter
from core.config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_schema), repo: UserRepository = Depends()):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        if datetime.now(UTC).timestamp() > payload.get("exp"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")

    user = await repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def get_file_storage() -> FileStorageAdapter:
    return S3FileStorageAdapter(
        bucket_name=settings.S3_BUCKET,
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
        url=settings.S3_URL,
    )