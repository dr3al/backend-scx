from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserCreate
from core.security import hash_password
from core.database import get_db


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_user_by_username(self, username: str):
        return await self.db.scalar(select(User).where(User.username == username))

    async def get_user_by_email(self, email: str):
        return await self.db.scalar(select(User).where(User.email == email))

    async def create_user(self, user: UserCreate):
        hashed_password = await hash_password(user.password)

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_avatar(self, user: User, avatar_url: str):
        user.avatar_url = avatar_url
        await self.db.commit()
        await self.db.refresh(user)
        return user