from fastapi import HTTPException, status
from models import TokenType
from datetime import datetime,timezone
from repositories.user_token_repository import get_token

from repositories.user_repository import get_user_by_id
from services.jwt_service import decode_token, create_access_token


def refresh_access_token(refresh_token: str, db):

    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    refresh_token_record = get_token(
        db=db,
        token=refresh_token,
        )

    if refresh_token_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    if refresh_token_record.token_type != TokenType.REFRESH_TOKEN:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid refresh token",
        )

    if refresh_token_record.used:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Refresh token has been revoked",
        )

    if refresh_token_record.expires_at < datetime.utcnow():
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Refresh token expired",
        )


    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been disabled",
        )

    access_token = create_access_token(
        user_id=str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }