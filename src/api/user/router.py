from fastapi import APIRouter, Depends
from src.api.user.schema import UserCreateInput
from src.api.user.service import UserService

router = APIRouter()

@router.get("/")
async def read_users(user_service : UserService = Depends()):
    users = user_service.get_users()
    return users

@router.post("/")
async def create_user(user_create_input: UserCreateInput, user_service :UserService = Depends()):
    user = user_service.create_user(user_create_input)
    return user

@router.get("/{user_id}")
async def read_user(user_id: int, user_service : UserService = Depends()):
    try:
        user = user_service.get_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
async def update_user(user_id: int, user_update_input: UserUpdateInput,user_service : UserService = Depends()):
    try:
        user = user_service.get_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
