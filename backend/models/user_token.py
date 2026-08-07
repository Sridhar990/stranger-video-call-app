import uuid
from datetime import datetime, timedelta

from sqlalchemy import String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from .enums import TokenType


class UserToken(Base):
    __tablename__ = "user_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    token_type: Mapped[TokenType] = mapped_column(
        Enum(TokenType),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,)
    

    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
    "User",
    back_populates="tokens",
)