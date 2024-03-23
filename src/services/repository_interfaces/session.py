from abc import ABC, abstractmethod
from typing import Optional
from src.dto.user import UserDTO


class ISessionRepository(ABC):
    @abstractmethod
    async def get(self, auth_token: str) -> Optional[UserDTO]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update(self, auth_token: str, user_data: UserDTO) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def set(self, auth_token: str, user_data: UserDTO) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def delete(self, auth_token: str) -> None:
        raise NotImplementedError("This method should be implemented")
