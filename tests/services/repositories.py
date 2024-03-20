import datetime
from typing import Optional
from src.dto.signin import SignInCreateDTO, SignDTO
from src.dto.user import UserCreateDTO, UserDTO
from src.services.repository_interfaces.session import ISessionRepository
from src.services.repository_interfaces.signin import ISignInRepository
from src.services.repository_interfaces.user import IUserRepository


class UserInMemoryRepository(IUserRepository):
    def __init__(self):
        self.users: list[UserDTO] = []
        self.next_id = 1

    async def add_one(self, data: UserCreateDTO) -> UserDTO:
        user_id = self.next_id
        self.next_id += 1
        user = UserDTO(
            id=user_id, name=data.name, email=data.email,
            user_created_at=datetime.datetime.utcnow(),
            hashed_password=data.hashed_password,
            salt=data.salt, password_updated_at=datetime.datetime.utcnow()
        )
        self.users.append(user)
        return user

    async def exist_by_name(self, name: str) -> bool:
        return any(user.name == name for user in self.users)

    async def exist_by_email(self, email: str) -> bool:
        return any(user.email == email for user in self.users)

    async def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = next((user for user in self.users if user.id == user_id), None)
        return user

    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        user = next((user for user in self.users if user.email == email), None)
        return user

    async def update_password(self, user_id: int, hashed_password: str, salt: str) -> None:
        user = await self.get_by_id(user_id)
        if user:
            user.hashed_password = hashed_password
            user.salt = salt
            user.password_updated_at = datetime.datetime.utcnow()

    async def update_name(self, user_id: int, name: str) -> None:
        user = await self.get_by_id(user_id)
        if user:
            user.name = name

    async def update_email(self, user_id: int, email: str) -> None:
        user = await self.get_by_id(user_id)
        if user:
            user.email = email

    async def delete_by_id(self, user_id: int) -> None:
        self.users = list(filter(lambda u: u.id != user_id, self.users))


class SignInInMemoryRepository(ISignInRepository):
    def __init__(self):
        self.next_id = 1
        self.signins: list[SignDTO] = []

    async def add_one(self, data: SignInCreateDTO) -> SignDTO:
        signin_id = self.next_id
        self.next_id += 1
        signin = SignDTO(
            id=signin_id, user_agent=data.user_agent,
            auth_token=data.auth_token, user_id=data.user_id,
            created_at=datetime.datetime.utcnow(),
            logout_at=None, is_logout=False
        )
        self.signins.append(signin)
        return signin

    async def get_by_auth_token(self, auth_token: str) -> Optional[SignDTO]:
        signin = next((signin for signin in self.signins if signin.auth_token == auth_token), None)
        return signin

    async def update_logout_status(self, auth_token: str, logout_date: datetime.datetime) -> None:
        signin = next((signin for signin in self.signins if signin.auth_token == auth_token), None)
        if signin:
            signin.logout_at = datetime.datetime.utcnow()
            signin.is_logout = True


class SessionInMemoryRepository(ISessionRepository):
    def __init__(self):
        self.data: dict[str:UserDTO] = dict()

    async def get(self, auth_token: str) -> Optional[UserDTO]:
        return self.data.get(auth_token)

    async def update(self, auth_token: str, user_data: UserDTO) -> None:
        self.data[auth_token] = user_data

    async def set(self, auth_token: str, user_data: UserDTO) -> None:
        self.data[auth_token] = user_data

    async def delete(self, auth_token: str) -> None:
        del self.data[auth_token]
