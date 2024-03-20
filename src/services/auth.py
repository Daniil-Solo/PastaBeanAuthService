import uuid
import datetime
from src.services.repository_interfaces.user import IUserRepository
from src.services.repository_interfaces.signin import ISignInRepository
from src.services.repository_interfaces.session import ISessionRepository
from src.dto.user import UserCreateDTO, UserDTO, UserLoginDTO, UserRegisterDTO, AuthDTO
from src.dto.signin import SignInCreateDTO
from src.services.exceptions import SuchUserExistsException, SuchUserDoesntExistException, PasswordIncorrectException, \
    NeedAuthException
from src.services.password import PasswordService


class AuthService:
    def __init__(self, user_repo: IUserRepository, signin_repo: ISignInRepository, session_repo: ISessionRepository):
        self.__user_repo = user_repo
        self.__signin_repo = signin_repo
        self.__session_repo = session_repo

    async def register_user(self, user_data: UserRegisterDTO) -> UserDTO:
        if await self.__user_repo.exist_by_name(user_data.name):
            raise SuchUserExistsException("Пользователь с таким именем уже существует")
        if await self.__user_repo.exist_by_email(user_data.email):
            raise SuchUserExistsException("Пользователь с таким email уже существует")
        PasswordService.validate_password(user_data.password)
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(user_data.password)
        user_data_with_password = UserCreateDTO(
            name=user_data.name, email=user_data.email,
            hashed_password=hashed_password, salt=salt
        )
        return await self.__user_repo.add_one(user_data_with_password)

    async def login(self, user_data: UserLoginDTO, user_agent: str) -> AuthDTO:
        existing_user = await self.__user_repo.get_by_email(user_data.email)
        if not existing_user:
            raise SuchUserDoesntExistException("Пользователя с таким email не существует")
        if not PasswordService.verify_password(user_data.password, existing_user.hashed_password, existing_user.salt):
            raise PasswordIncorrectException("Пароль неверный")
        auth_token = uuid.uuid4().hex
        signin = await self.__signin_repo.add_one(
            SignInCreateDTO(user_agent=user_agent, auth_token=auth_token, user_id=existing_user.id)
        )
        await self.__session_repo.set(auth_token, existing_user)
        return AuthDTO(user=existing_user, auth_token=signin.auth_token)

    async def logout(self, auth_token: str) -> None:
        await self.__signin_repo.update_logout_status(auth_token, datetime.datetime.utcnow())
        await self.__session_repo.delete(auth_token)

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
