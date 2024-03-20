from abc import ABC, abstractmethod
from typing import Optional
from src.dto.user import UserCreateDTO, UserDTO


class IUserRepository(ABC):
    @abstractmethod
    async def add_one(self, data: UserCreateDTO) -> UserDTO:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def exist_by_name(self, name: str) -> bool:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def exist_by_email(self, email: str) -> bool:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update_password(self, user_id: int, hashed_password: str, salt: str) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update_name(self, user_id: int, name: str) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update_email(self, user_id: int, email: str) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def delete_by_id(self, user_id: int) -> None:
        raise NotImplementedError("This method should be implemented")
