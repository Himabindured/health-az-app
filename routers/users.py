from fastapi import APIRouter, Depends
from schemas.schemas import UserOut
from models.models import User
from auth_utils import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
