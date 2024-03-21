from fastapi import Header, Depends
from fastapi import status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_async_session
from src.cache.session import get_redis_session
from src.endpoints.exceptions import ApplicationException
from src.services.auth import AuthService
from src.cache.repositories.session import SessionRedisRepository
from src.database.repositories.user import UserSQLARepository
from src.database.repositories.signin import SignInSQLARepository


def get_auth_service(
        cache_session: Redis = Depends(get_redis_session),
        db_session: AsyncSession = Depends(get_async_session),
) -> AuthService:
    user_repo = UserSQLARepository(db_session)
    signin_repo = SignInSQLARepository(db_session)
    session_repo = SessionRedisRepository(cache_session)
    return AuthService(user_repo, signin_repo, session_repo)


def get_auth_token(authorization: str = Header(None, alias="Authorization")) -> str:
    if not authorization:
        raise ApplicationException(
            "Для выполнения действия требуется войти в аккаунт",
            status.HTTP_401_UNAUTHORIZED
        )
    auth_token = authorization.lstrip("Bearer").strip()
    return auth_token
