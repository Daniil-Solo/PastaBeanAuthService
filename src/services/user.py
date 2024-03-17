from src.services.exceptions import SuchUserExistsException, NeedAuthException
from src.services.password import PasswordService
from src.services.repository_interfaces.session import ISessionRepository
from src.services.repository_interfaces.user import IUserRepository
from src.dto.user import UserDTO


class UserService:
    def __init__(self, user_repo: IUserRepository, session_repo: ISessionRepository):
        self.__user_repo = user_repo
        self.__session_repo = session_repo

    async def get_user(self, auth_token: str) -> UserDTO:
        user_dto = await self.__session_repo.get(auth_token)
        if not user_dto:
            raise NeedAuthException("Требуется авторизация")
        return user_dto

    async def change_name(self, auth_token: str, user_data: UserDTO, new_name: str) -> None:
        if await self.__user_repo.exist_by_name(new_name):
            raise SuchUserExistsException("Пользователь с таким именем уже существует")
        await self.__user_repo.update_name(user_data.id, new_name)
        user_data.name = new_name
        await self.__session_repo.set(auth_token, user_data)

    async def change_email(self, auth_token: str, user_data: UserDTO, new_email: str) -> None:
        if await self.__user_repo.exist_by_email(new_email):
            raise SuchUserExistsException("Пользователь с таким email уже существует")
        await self.__user_repo.update_email(user_data.id, new_email)
        user_data.email = new_email
        await self.__session_repo.set(auth_token, user_data)

    async def change_password(self, auth_token: str, user_data: UserDTO, new_password: str) -> None:
        PasswordService.validate_password(new_password)
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(new_password)
        await self.__user_repo.update_password(user_data.id, hashed_password, salt)
        user_data.hashed_password = hashed_password
        user_data.salt = salt
        await self.__session_repo.update(auth_token, user_data)
