# tests/conftest.py
import os
from sqlalchemy import text

os.environ["ENV"] = "test"
os.environ["TESTING"] = "true"

import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient
from core.rate_limit import limiter

from main import app
from tests.testing_database import TestingSessionLocal,engine
from dependencies import get_db
from database import Base
from tests.mocks import mock_send_verification_email,mock_send_password_reset_email


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch(
            "services.auth_service.send_verification_email",
            new=mock_send_verification_email,
        ), patch(
            "services.forgot_password_service.send_password_reset_email",
            new=mock_send_password_reset_email,
        ), patch(
            "services.resend_verification_service.send_verification_email",
            new=mock_send_verification_email,
        ):
            with TestClient(app) as client:
                yield client

    finally:
        app.dependency_overrides.clear()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@pytest.fixture(autouse=True)
def cleanup_database(db):
    yield

    db.execute(
        text("""
        TRUNCATE TABLE
            user_tokens,
            users
        RESTART IDENTITY CASCADE;
        """)
    )

    db.commit()

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)





@pytest.fixture
def enable_rate_limiter():
    previous_state = limiter.enabled
    limiter.enabled = True

    yield

    limiter.enabled = previous_state