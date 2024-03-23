from typing import Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.dto.user import UserCreateDTO, UserDTO
from src.database.models import User, SecureUserInfo
from src.services.repository_interfaces.user import IUserRepository


class UserSQLARepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_one(self, data: UserCreateDTO) -> UserDTO:
        user = User(name=data.name, email=data.email)
        secure_info = SecureUserInfo(hashed_password=data.hashed_password, salt=data.salt)
        secure_info.user = user
        self.__session.add(secure_info)
        await self.__session.commit()
        await self.__session.refresh(user)
        await self.__session.refresh(secure_info)
        return UserDTO(
            id=user.id, name=user.name, email=user.email,
            user_created_at=user.created_at, salt=secure_info.salt,
            hashed_password=secure_info.hashed_password,
            password_updated_at=secure_info.updated_at
        )

    async def exist_by_name(self, name: str) -> bool:
        user = await self.__get_by_field(field_name="name", field_value=name)
        return user is not None

    async def exist_by_email(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None

    async def __get_by_field(self, field_name: str, field_value: any) -> Optional[UserDTO]:
        query = (
            select(User)
            .filter_by(**{field_name: field_value})
            .options(joinedload(User.secure_info))
        )
        result = await self.__session.execute(query)
        user = result.scalar_one_or_none()
        return UserDTO(
            id=user.id, name=user.name, email=user.email, user_created_at=user.created_at,
            hashed_password=user.secure_info.hashed_password, salt=user.secure_info.salt,
            password_updated_at=user.secure_info.updated_at
        ) if user else None

    async def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        return await self.__get_by_field(field_name="id", field_value=user_id)

    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        return await self.__get_by_field(field_name="email", field_value=email)

    async def update_password(self, user_id: int, hashed_password: str, salt: str) -> None:
        stmt = (
            update(SecureUserInfo)
            .values({SecureUserInfo.hashed_password: hashed_password, SecureUserInfo.salt: salt})
            .where(SecureUserInfo.user_id == user_id)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def update_name(self, user_id: int, name: str) -> None:
        stmt = update(User).values({User.name: name}).where(User.id == user_id)
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def update_email(self, user_id: int, email: str) -> None:
        stmt = update(User).values({User.email: email}).where(User.id == user_id)
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def delete_by_id(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.__session.execute(stmt)
        await self.__session.commit()
