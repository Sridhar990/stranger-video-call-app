import secrets
from datetime import datetime, timedelta
from services.jwt_service import create_refresh_token
from config import REFRESH_TOKEN_EXPIRE_DAYS
from sqlalchemy.orm import Session

from config import (
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS,
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
)
from models import User, UserToken, TokenType
from repositories.user_token_repository import create_user_token


def generate_user_token(
    db: Session,
    user: User,
    token_type: TokenType,
):
    token = secrets.token_urlsafe(32)

    if token_type == TokenType.EMAIL_VERIFICATION:
        expires_at = datetime.utcnow() + timedelta(
            hours=EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS
        )

    elif token_type == TokenType.PASSWORD_RESET:
        expires_at = datetime.utcnow() + timedelta(
            minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )

    else:
        raise ValueError("Invalid token type")

    new_token = UserToken(
        user_id=user.id,
        token=token,
        token_type=token_type,
        expires_at=expires_at,
    )

    create_user_token(
        db=db,
        user_token=new_token,
    )

    return new_token


def create_refresh_token_record(
    db: Session,
    user: User,
):
    refresh_token = create_refresh_token(
        user_id=str(user.id),
    )

    refresh_token_record = UserToken(
        user_id=user.id,
        token=refresh_token,
        token_type=TokenType.REFRESH_TOKEN,
        expires_at=datetime.utcnow()
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    create_user_token(
        db=db,
        user_token=refresh_token_record,
    )

    return refresh_token