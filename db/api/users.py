from fastapi import APIRouter, UploadFile, File, Depends, status

from core.depends import get_current_user
from models import User
from schemas import UserResponse
from services import UserService

router = APIRouter(tags=["users"])

@router.put("/me/avatar", response_model=UserResponse, status_code=status.HTTP_200_OK)
def upload_avatar(
    file: UploadFile = File(..., description="Картинка jpg, png"),
    current_user: User = Depends(get_current_user),
    service: UserService = Depends()
):
    return service.upload_avatar(user=current_user, file=file)
