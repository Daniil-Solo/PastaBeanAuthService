import datetime

from pydantic import BaseModel


class SignInCreateDTO(BaseModel):
    user_agent: str
    auth_token: str
    user_id: int


class SignDTO(BaseModel):
    id: int
    user_agent: str
    auth_token: str
    created_at: datetime.datetime
    user_id: int
