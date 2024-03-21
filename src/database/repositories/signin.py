import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import SignIn
from src.dto.signin import SignInCreateDTO, SignDTO
from src.services.repository_interfaces.signin import ISignInRepository


class SignInSQLARepository(ISignInRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_one(self, data: SignInCreateDTO) -> SignDTO:
        signin = SignIn(**data.dict())
        self.__session.add(signin)
        await self.__session.commit()
        await self.__session.refresh(signin)
        return SignDTO.model_validate(signin, from_attributes=True)

    async def get_by_auth_token(self, auth_token: str) -> Optional[SignDTO]:
        query = select(SignIn).where(SignIn.auth_token == auth_token)
        result = await self.__session.execute(query)
        signin = result.scalar_one_or_none()
        return SignDTO.model_validate(signin, from_attributes=True) if signin is not None else None

    async def update_logout_status(self, auth_token: str, logout_date: datetime.datetime) -> None:
        stmt = (
            update(SignIn)
            .values({SignIn.is_logout: True, SignIn.logout_at: logout_date})
            .where(SignIn.auth_token == auth_token)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
