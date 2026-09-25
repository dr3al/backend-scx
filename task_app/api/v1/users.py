from fastapi import APIRouter
from schemas import CreateUserRequest, UserResponse, TaskIn

users = []

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
    try:
        user = users[user_id-1]
    except IndexError:
        return {"error": "user not found"}

    return UserResponse(user)