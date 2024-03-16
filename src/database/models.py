import datetime
from sqlalchemy import text, ForeignKey
from src.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SecureUserInfo(Base):
    __tablename__ = "secure_user_infos"

    id: Mapped[int] = mapped_column(primary_key=True)
    hashed_password: Mapped[str]
    salt: Mapped[str]
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="secure_info")


class SignIn(Base):
    __tablename__ = "sign_ins"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_agent: Mapped[str]
    auth_token: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    is_logout: Mapped[bool] = mapped_column(default=False)
    logout_at: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sign_ins")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    secure_info: Mapped[SecureUserInfo] = relationship(
        back_populates="user", uselist=False
    )
    sign_ins: Mapped[list[SignIn]] = relationship(back_populates="user")
