from fastapi import APIRouter, Body, Depends, Header
from src.endpoints.dependencies import get_auth_token, get_auth_service
from src.dto.user import UserRegisterDTO, UserLoginDTO
from src.endpoints.schemas import LoginResponse
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(
        register_data: UserRegisterDTO = Body(),
        service: AuthService = Depends(get_auth_service)
):
    await service.register_user(register_data)
    return {"status": "ok"}


@router.post("/login", response_model=LoginResponse)
async def login(
        login_data: UserLoginDTO = Body(),
        service: AuthService = Depends(get_auth_service),
        user_agent: str = Header(None, alias="User-Agent")
):
    print(user_agent)
    auth_data = await service.login(login_data, user_agent)
    return LoginResponse.from_auth_dto(auth_data)


@router.post("/logout")
async def logout(
        service: AuthService = Depends(get_auth_service),
        auth_token: str = Depends(get_auth_token)
):
    await service.logout(auth_token)
    return {"status": "ok"}
