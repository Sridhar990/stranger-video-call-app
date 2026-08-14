from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,status
from jose import jwt,JWTError

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


def create_token(
        user_id:str,
        token_type:str,
        expire_delta: timedelta
):
    expire= datetime.now(timezone.utc) + expire_delta

    playload= {
        "sub": str(user_id),
        "type": token_type,
        "exp": expire
               }

    return jwt.encode(playload,SECRET_KEY,algorithm=ALGORITHM)


def create_access_token(user_id: str):
    return create_token(
        user_id=user_id,
        token_type="access",
        expire_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

def create_refresh_token(user_id: str):
    return create_token(
        user_id=user_id,
        token_type="refresh",
        expire_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS,
        )
    )

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )