from models import User
from services.jwt_service import (
    create_access_token,
    create_refresh_token,
)
from utils import hash_password


def test_get_me_success(client, db):
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

    access_token = create_access_token(user_id=str(user.id))

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == "sridhar"
    assert body["email"] == "sridhar@test.com"

def test_get_me_missing_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_me_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid.jwt.token",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or expired token",
    }


def test_get_me_refresh_token(client, db):
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

    refresh_token = create_refresh_token(
        user_id=str(user.id)
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {refresh_token}",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid token type",
    }


def test_get_me_user_not_found(client):
    access_token = create_access_token(
        user_id="11111111-1111-1111-1111-111111111111"
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "User not found",
    }


def test_get_me_email_not_verified(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=False,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        user_id=str(user.id)
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Please verify your email",
    }


def test_get_me_account_disabled(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        user_id=str(user.id)
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Your account has been disabled",
    }