from fastapi import APIRouter
from dependencies.user_dependencies import user_service_dep

user_router = APIRouter(prefix="/user")

@user_router.get("/{user_id}")
async def get_user(user_id: str, user_service: user_service_dep):
    return user_service.get_user(user_id)