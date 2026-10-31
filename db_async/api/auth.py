from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.util import await_

from core.security import verify_password, create_access_token
from core.depends import get_current_user
from schemas.users import UserResponse, UserCreate, Token
from repositories.users import UserRepository
from models import User
from core.exceptions import EmailAlreadyRegisteredException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, repo: UserRepository = Depends()):
    if await repo.get_user_by_email(user.email):
        raise EmailAlreadyRegisteredException(user.email)
    if await repo.get_user_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return await repo.create_user(user)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repo: UserRepository = Depends()):
    user = await repo.get_user_by_username(form_data.username)

    if not user or not await verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or username",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token({
        "username": user.username,
        "user_id": user.id,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
