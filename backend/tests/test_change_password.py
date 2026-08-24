from models import User
from services.jwt_service import create_access_token
from utils import hash_password, verify_password


def test_change_password_success(client, db):
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

    access_token = create_access_token(
        user_id=str(user.id),
    )

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Password changed successfully",
    }

    db.refresh(user)
    assert verify_password(
        "NewPassword@123",
        user.password,
    )



def test_change_password_missing_token(client):
    response = client.post(
        "/auth/change-password",
        json={
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 401


def test_change_password_invalid_token(client):
    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": "Bearer invalid.jwt.token",
        },
        json={
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or expired token",
    }


def test_change_password_wrong_current_password(client, db):
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

    access_token = create_access_token(
        user_id=str(user.id),
    )

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "current_password": "WrongPassword@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Current password is incorrect",
    }


def test_change_password_same_password(client, db):
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

    access_token = create_access_token(
        user_id=str(user.id),
    )

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "current_password": "Password@123",
            "new_password": "Password@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "New password must be different from current password",
    }


def test_change_password_email_not_verified(client, db):
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
        user_id=str(user.id),
    )

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Please verify your email",
    }


def test_change_password_account_disabled(client, db):
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
        user_id=str(user.id),
    )

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Your account has been disabled",
    }