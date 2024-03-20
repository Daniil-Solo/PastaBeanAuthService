import datetime
from abc import ABC, abstractmethod
from typing import Optional
from src.dto.signin import SignDTO, SignInCreateDTO


class ISignInRepository(ABC):
    @abstractmethod
    async def add_one(self, data: SignInCreateDTO) -> SignDTO:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_by_auth_token(self, auth_token: str) -> Optional[SignDTO]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update_logout_status(self, auth_token: str, logout_date: datetime.datetime) -> None:
        raise NotImplementedError("This method should be implemented")
