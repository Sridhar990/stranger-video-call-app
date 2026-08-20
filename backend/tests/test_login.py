from models import User
from utils import hash_password


def test_login_success(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


def test_login_email_not_registered(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password",
    }


def test_login_wrong_password(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password",
    }


def test_login_email_not_verified(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=False,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Please verify your email",
    }


def test_login_account_disabled(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=False,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Your account has been disabled",
    }


def test_login_email_normalization(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "  SRIDHAR@TEST.COM  ",
            "password": "Password@123",
        },
    )

    assert response.status_code == 200


def test_login_returns_non_empty_tokens(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    data = response.json()

    assert data["access_token"] != ""
    assert data["refresh_token"] != ""



def test_login_token_types(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    data = response.json()

    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)

def test_login_access_and_refresh_tokens_are_different(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    data = response.json()

    assert data["access_token"] != data["refresh_token"]

def test_login_email_trim_only(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "   sridhar@test.com   ",
            "password": "Password@123",
        },
    )

    assert response.status_code == 200