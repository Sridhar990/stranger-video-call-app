from models import User
from services.jwt_service import create_refresh_token
from utils import hash_password


def create_user(db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_login_rate_limit(client, db, enable_rate_limiter):
    create_user(db)

    payload = {
        "email": "sridhar@test.com",
        "password": "Password@123",
    }

    for _ in range(6):
        response = client.post("/auth/login", json=payload)

    assert response.status_code == 429


def test_register_rate_limit(client, enable_rate_limiter):
    for i in range(6):
        payload = {
            "username": f"username{i}",
            "email": f"user{i}@test.com",
            "password": "Password@123",
        }
        response = client.post("/auth/register", json=payload)

    assert response.status_code == 429


def test_refresh_rate_limit(client, enable_rate_limiter):
    payload = {
        "refresh_token": "invalid-token",
    }

    for _ in range(11):
        response = client.post("/auth/refresh", json=payload)

    assert response.status_code == 429


def test_forgot_password_rate_limit(client, enable_rate_limiter):
    payload = {
        "email": "unknown@test.com",
    }

    for _ in range(4):
        response = client.post("/auth/forgot-password", json=payload)

    assert response.status_code == 429


def test_reset_password_rate_limit(client, enable_rate_limiter):
    payload = {
        "token": "invalid-token",
        "new_password": "Password@123",
    }

    for _ in range(6):
        response = client.post("/auth/reset-password", json=payload)

    assert response.status_code == 429


def test_resend_verification_rate_limit(client, enable_rate_limiter):
    payload = {
        "email": "unknown@test.com",
    }

    for _ in range(4):
        response = client.post("/auth/resend-verification", json=payload)

    assert response.status_code == 429