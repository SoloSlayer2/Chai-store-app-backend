from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
    event,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timedelta, timezone
import decimal
import uuid
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("email", name="users_email_key"),
        UniqueConstraint("username", name="users_username_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    def isPasswordCorrect(self, password) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def generateAccessToken(self) -> str:
        payload = {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    def generateRefreshToken(self) -> str:
        payload = {
            "id": str(self.id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


# Pre Save Hooks
# @event.listens_for(Users, "before_insert")
# def hashUserPassword(mapper, connection, target):
#     if target.hashed_password:
#         target.hashed_password = pwd_context.hash(target.hashed_password)


# @event.listens_for(Users, "before_update")
# def rehashIfPasswordChanged(mapper, connection, target):
#     state = inspect(target)
#     hist = state.attrs.hashed_password.history
#     if not hist.has_changes():
#         return  # ✅ Password was not modified
#     target.hashed_password = pwd_context.hash(target.hashed_password)

#Problem was using this pre save hook if the old password matched the new password then the rehash would fail silently so we hash it in the reset password itself
