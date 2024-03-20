import pytest
from src.dto.user import UserCreateDTO, UserRegisterDTO
from src.services.auth import AuthService
from src.services.password import PasswordService
from src.services.repository_interfaces.user import IUserRepository
from tests.services.repositories import UserInMemoryRepository, SignInInMemoryRepository, SessionInMemoryRepository


@pytest.fixture
def user_register_data() -> UserRegisterDTO:
    return UserRegisterDTO(
        name="Antonio",
        email="antonio@mail.ru",
        password="anton1412"
    )


@pytest.fixture
def empty_auth_service() -> AuthService:
    user_repo = UserInMemoryRepository()
    signin_repo = SignInInMemoryRepository()
    session_repo = SessionInMemoryRepository()
    return AuthService(user_repo, signin_repo, session_repo)


@pytest.fixture
async def user_repo_with_user(user_register_data: UserRegisterDTO) -> IUserRepository:
    hashed_password, salt = PasswordService.create_hashed_password_and_salt(user_register_data.password)
    user_create_data = UserCreateDTO(
        **user_register_data.model_dump(),
        hashed_password=hashed_password,
        salt=salt
    )
    user_repo = UserInMemoryRepository()
    await user_repo.add_one(user_create_data)
    return user_repo


@pytest.fixture
def auth_service_with_user(user_repo_with_user: IUserRepository) -> AuthService:
    signin_repo = SignInInMemoryRepository()
    session_repo = SessionInMemoryRepository()
    return AuthService(user_repo_with_user, signin_repo, session_repo)
