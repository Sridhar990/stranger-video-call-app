from repositories.user_repository import get_user_by_email
from fastapi import HTTPException,status
from sqlalchemy.orm import Session 
from schemas.user import LoginRequest
from utils import verify_password
from .jwt_service import (
    create_access_token,
    create_refresh_token,
)
from datetime import datetime, timedelta

from models import UserToken, TokenType
from repositories.user_token_repository import create_user_token
from config import REFRESH_TOKEN_EXPIRE_DAYS



async def login_user(user:LoginRequest,db:Session):
    # Normailze email 
    email= user.email.lower().strip()

    # find user

    existing_user = get_user_by_email(db=db,email=email)

    # check if user exist

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")


    # verify password 

    if not verify_password(user.password,existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")


    # email verification 

    if not existing_user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please verify your email")


    # check user is active

    if not existing_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Your account has been disabled")



    access_token = create_access_token(user_id=str(existing_user.id))
    refresh_token= create_refresh_token(user_id=str(existing_user.id))

    refresh_token_record = UserToken(
    user_id=existing_user.id,
    token=refresh_token,
    token_type=TokenType.REFRESH_TOKEN,
    expires_at=datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    ),
)
    create_user_token(
        db=db,
        user_token=refresh_token_record,
    )


    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "Bearer",
}