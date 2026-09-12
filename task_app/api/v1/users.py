from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field, field_validator

users = []


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=32)
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif value in ("password", "pass1234"):
            raise ValueError("Password is too easy")
        # elif value != cls.:
        #     raise ValueError("Password can't be same as username")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


router = APIRouter()

@router.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: CreateUserRequest):
    user = {
        "id": len(users) + 1,
        "email": user.email,
        "username": user.username,
        "password": user.password
    }
    users.append(user)

    return user

@router.get("/users/{user_id}", status_code=200)
def get_user(user_id: int):
    user = users[user_id]

    user.pop("password")

    return user