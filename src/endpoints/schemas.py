import datetime
from pydantic import BaseModel
from src.dto.user import AuthDTO


class LoginResponse(BaseModel):
    name: str
    email: str
    user_created_at: datetime.datetime
    password_updated_at: datetime.datetime
    auth_token: str

    @staticmethod
    def from_auth_dto(auth_data: AuthDTO) -> "LoginResponse":
        return LoginResponse(
            name=auth_data.user.name,
            email=auth_data.user.email,
            user_created_at=auth_data.user.user_created_at,
            password_updated_at=auth_data.user.password_updated_at,
            auth_token=auth_data.auth_token,
        )
