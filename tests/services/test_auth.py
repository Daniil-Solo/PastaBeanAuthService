import pytest
from src.dto.user import UserRegisterDTO, UserLoginDTO
from src.services.auth import AuthService
from src.services.exceptions import SuchUserExistsException, SuchUserDoesntExistException, PasswordIncorrectException


class TestUserRegistrator:
    async def test_existing_name(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        user_register_data = UserRegisterDTO(
            name=user_register_data.name,
            email="some@mail.ru",
            password="somepassword123"
        )
        with pytest.raises(SuchUserExistsException):
            await auth_service_with_user.register_user(user_register_data)

    async def test_existing_email(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        user_register_data = UserRegisterDTO(
            name="some",
            email=user_register_data.email,
            password="somepassword123"
        )
        with pytest.raises(SuchUserExistsException):
            await auth_service_with_user.register_user(user_register_data)

    async def test_success_adding_user(self, empty_auth_service: AuthService, user_register_data: UserRegisterDTO):
        await empty_auth_service.register_user(user_register_data)


class TestUserLogin:
    async def test_non_existing_email(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        login_user_data = UserLoginDTO(
            email="new@mail.ru",
            password="asdas221"
        )
        with pytest.raises(SuchUserDoesntExistException):
            await auth_service_with_user.login(login_user_data, "")

    async def test_incorrect_password(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        login_user_data = UserLoginDTO(
            email=user_register_data.email,
            password="asdas221"
        )
        with pytest.raises(PasswordIncorrectException):
            await auth_service_with_user.login(login_user_data, "")

    async def test_success_login(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        login_user_data = UserLoginDTO(
            email=user_register_data.email,
            password=user_register_data.password
        )
        await auth_service_with_user.login(login_user_data, "")


class TestUserLogout:
    async def test_success_logout(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        login_user_data = UserLoginDTO(
            email=user_register_data.email,
            password=user_register_data.password
        )
        auth_data = await auth_service_with_user.login(login_user_data, "")
        await auth_service_with_user.logout(auth_data.auth_token)
