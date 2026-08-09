from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User, TokenType
from schemas.user import UserCreate
from utils import hash_password
from repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    create_user,
)
from services.token_service import generate_user_token
from services.email_service import send_verification_email
from config import FRONTEND_URL


async def register_user(
    user: UserCreate,
    db: Session,
):
    # Normalize input
    email = user.email.lower().strip()
    username = user.username.lower().strip()

    # Check email
    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check username
    if get_user_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create user object
    new_user = User(
        email=email,
        username=username,
        password=hash_password(user.password),
    )

    # Save user
    create_user(db, new_user)

    # Generate verification token
    user_token = generate_user_token(
        db=db,
        user=new_user,
        token_type=TokenType.EMAIL_VERIFICATION,
    )

    # Build verification link
    verification_link = (
        f"{FRONTEND_URL}/verify-email?token={user_token.token}"
    )

    # Send verification email
    await send_verification_email(
        email=new_user.email,
        username=new_user.username,
        verification_link=verification_link,
    )

    return {
        "message": "User registered successfully. Please verify your email."
    }