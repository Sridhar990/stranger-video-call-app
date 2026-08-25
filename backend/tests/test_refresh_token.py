from datetime import datetime, timedelta

from models import User, UserToken, TokenType
from repositories.user_token_repository import get_token
from services.jwt_service import (
    create_refresh_token,
    create_access_token,
)
from utils import hash_password


def create_refresh_user(
    db,
    *,
    is_verified=True,
    is_active=True,
    token_type=TokenType.REFRESH_TOKEN,
    used=False,
    expires_at=None,
):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=is_verified,
        is_active=is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token(
        user_id=str(user.id)
    )

    if expires_at is None:
        expires_at = datetime.utcnow() + timedelta(days=7)

    user_token = UserToken(
        user_id=user.id,
        token=refresh_token,
        token_type=token_type,
        expires_at=expires_at,
        used=used,
    )
    db.add(user_token)
    db.commit()
    db.refresh(user_token)

    return user, user_token


def test_refresh_token_success(client, db):
    _, user_token = create_refresh_user(db)

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != user_token.token
    assert data["token_type"] == "Bearer"

    # Old refresh token should be revoked
    db.refresh(user_token)
    assert user_token.used is True

    # New refresh token should be stored
    new_token = get_token(
        db=db,
        token=data["refresh_token"],
    )

    assert new_token is not None
    assert new_token.used is False
    assert new_token.user_id == user_token.user_id
    assert new_token.token_type == TokenType.REFRESH_TOKEN


def test_refresh_token_cannot_be_reused(client, db):
    _, user_token = create_refresh_user(db)

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Refresh token has been revoked"
    }


def test_refresh_token_invalid_jwt(client):
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "invalid-token",
        },
    )

    assert response.status_code == 401


def test_refresh_token_wrong_token_type(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        user_id=str(user.id)
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": access_token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid refresh token"
    }


def test_refresh_token_not_found(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token(
        user_id=str(user.id)
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid refresh token"
    }


def test_refresh_token_revoked(client, db):
    _, user_token = create_refresh_user(
        db,
        used=True,
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Refresh token has been revoked"
    }


def test_refresh_token_expired(client, db):
    _, user_token = create_refresh_user(
        db,
        expires_at=datetime.utcnow() - timedelta(hours=1),
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Refresh token expired"
    }


def test_refresh_token_email_not_verified(client, db):
    _, user_token = create_refresh_user(
        db,
        is_verified=False,
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Please verify your email"
    }


def test_refresh_token_account_disabled(client, db):
    _, user_token = create_refresh_user(
        db,
        is_active=False,
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": user_token.token,
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Your account has been disabled"
    }