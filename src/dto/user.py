import datetime
from pydantic import BaseModel


class UserRegisterDTO(BaseModel):
    name: str
    email: str
    password: str


class UserLoginDTO(BaseModel):
    email: str
    password: str


class UserCreateDTO(BaseModel):
    name: str
    email: str
    hashed_password: str
    salt: str


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    user_created_at: datetime.datetime
    hashed_password: str
    salt: str
    password_updated_at: datetime.datetime


class AuthDTO(BaseModel):
    user: UserDTO
    auth_token: str
