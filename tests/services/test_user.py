import pytest
from src.dto.user import UserRegisterDTO, UserLoginDTO, AuthDTO
from src.services.auth import AuthService
from src.services.exceptions import NeedAuthException


class TestUserService:
    @staticmethod
    async def get_auth_data(auth_service: AuthService, user: UserRegisterDTO) -> AuthDTO:
        auth_data = await auth_service.login(
            UserLoginDTO(email=user.email, password=user.password),
            "some-user-agent"
        )
        return auth_data

    async def test_incorrect_auth_token(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        auth_token = ""
        with pytest.raises(NeedAuthException):
            await auth_service_with_user.get_user(auth_token)

    async def test_correct_auth_token(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        auth_data = await self.get_auth_data(auth_service_with_user, user_register_data)
        await auth_service_with_user.get_user(auth_data.auth_token)

    async def test_change_password(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        auth_data = await self.get_auth_data(auth_service_with_user, user_register_data)
        new_password = user_register_data.password + "!"
        await auth_service_with_user.change_password(auth_data.auth_token, auth_data.user, new_password)
        new_user_data = await auth_service_with_user.get_user(auth_data.auth_token)
        assert new_user_data.hashed_password == auth_data.user.hashed_password
        assert new_user_data.salt == auth_data.user.salt

    async def test_change_name(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        auth_data = await self.get_auth_data(auth_service_with_user, user_register_data)
        new_name = "Newman"
        await auth_service_with_user.change_name(auth_data.auth_token, auth_data.user, new_name)
        new_user_data = await auth_service_with_user.get_user(auth_data.auth_token)
        assert new_user_data.name == auth_data.user.name

    async def test_change_email(self, auth_service_with_user: AuthService, user_register_data: UserRegisterDTO):
        auth_data = await self.get_auth_data(auth_service_with_user, user_register_data)
        new_email = "newman@mail.ru"
        await auth_service_with_user.change_email(auth_data.auth_token, auth_data.user, new_email)
        new_user_data = await auth_service_with_user.get_user(auth_data.auth_token)
        assert new_user_data.email == auth_data.user.email
