from fastapi import APIRouter, Body, Depends
from src.endpoints.dependencies import get_auth_token, get_auth_service
from src.dto.user import UserDTO
from src.services.auth import AuthService

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/", response_model=UserDTO)
async def get_user(
        auth_token: str = Depends(get_auth_token),
        service: AuthService = Depends(get_auth_service),
):
    user_data = await service.get_user(auth_token)
    return user_data


@router.post("/change_password")
async def change_password(
        new_password: str = Body(embed=True),
        service: AuthService = Depends(get_auth_service),
        auth_token: str = Depends(get_auth_token)
):
    user_data = await service.get_user(auth_token)
    await service.change_password(auth_token, user_data, new_password)
    return {"status": "ok"}


@router.post("/change_name")
async def change_name(
        new_name: str = Body(embed=True),
        service: AuthService = Depends(get_auth_service),
        auth_token: str = Depends(get_auth_token)
):
    user_data = await service.get_user(auth_token)
    await service.change_name(auth_token, user_data, new_name)
    return {"status": "ok"}


@router.post("/change_email")
async def change_email(
        new_email: str = Body(embed=True),
        service: AuthService = Depends(get_auth_service),
        auth_token: str = Depends(get_auth_token)
):
    user_data = await service.get_user(auth_token)
    await service.change_email(auth_token, user_data, new_email)
    return {"status": "ok"}
