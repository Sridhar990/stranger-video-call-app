from datetime import datetime, timedelta

from models import User, UserToken, TokenType
from repositories.user_token_repository import create_user_token
from services.jwt_service import create_refresh_token
from utils import hash_password


def test_logout_success(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token(user_id=str(user.id))

    user_token = UserToken(
        user_id=user.id,
        token=refresh_token,
        token_type=TokenType.REFRESH_TOKEN,
        expires_at=datetime.utcnow() + timedelta(days=7),
        used=False,
    )

    create_user_token(
        db=db,
        user_token=user_token,
    )

    response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Logged out successfully"
    }

    db.refresh(user_token)
    assert user_token.used is True


def test_logout_invalid_refresh_token(client):
    response = client.post(
        "/auth/logout",
        json={
            "refresh_token": "invalid_token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid refresh token"
    }


def test_logout_already_revoked_token(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token(user_id=str(user.id))

    user_token = UserToken(
        user_id=user.id,
        token=refresh_token,
        token_type=TokenType.REFRESH_TOKEN,
        expires_at=datetime.utcnow() + timedelta(days=7),
        used=True,
    )

    create_user_token(
        db=db,
        user_token=user_token,
    )

    response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Refresh token already revoked"
    }

def test_logout_expired_refresh_token(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token(user_id=str(user.id))

    user_token = UserToken(
        user_id=user.id,
        token=refresh_token,
        token_type=TokenType.REFRESH_TOKEN,
        expires_at=datetime.utcnow() - timedelta(minutes=1),
        used=False,
    )

    create_user_token(
        db=db,
        user_token=user_token,
    )

    response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401