import datetime
import json
from typing import Optional
from redis.asyncio import Redis
from src.constants import AUTH_TOKEN_TTL
from src.dto.user import UserDTO
from src.services.repository_interfaces.session import ISessionRepository


class SessionRedisRepository(ISessionRepository):
    def __init__(self, session: Redis):
        self.__session = session

    @staticmethod
    def __from_user_dto_to_json_string(data: UserDTO) -> str:
        user_dict = data.dict()
        user_dict["user_created_at"] = str(user_dict["user_created_at"])
        user_dict["password_updated_at"] = str(user_dict["password_updated_at"])
        user_data_string = json.dumps(user_dict)
        return user_data_string

    async def get(self, auth_token: str) -> Optional[UserDTO]:
        user_dto = None
        try:
            user_data_string = await self.__session.get(auth_token)
            user_dict = json.loads(user_data_string)
            user_dict["user_created_at"] = datetime.datetime.fromisoformat((user_dict["user_created_at"]))
            user_dict["password_updated_at"] = datetime.datetime.fromisoformat((user_dict["password_updated_at"]))
            user_dto = UserDTO(**user_dict)
        except TypeError:  # no such key in Redis
            pass
        except json.decoder.JSONDecodeError:  # not json-format in returning value
            pass
        finally:
            return user_dto

    async def update(self, auth_token: str, user_data: UserDTO) -> None:
        user_data_string = self.__from_user_dto_to_json_string(user_data)
        remaining_ttl = await self.__session.ttl(auth_token)
        await self.__session.set(auth_token, user_data_string, keepttl=remaining_ttl)

    async def set(self, auth_token: str, user_data: UserDTO) -> None:
        user_data_string = self.__from_user_dto_to_json_string(user_data)
        await self.__session.set(auth_token, user_data_string, keepttl=AUTH_TOKEN_TTL)

    async def delete(self, auth_token: str) -> None:
        await self.__session.delete(auth_token)
