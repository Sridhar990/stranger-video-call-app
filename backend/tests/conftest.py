# tests/conftest.py
import os

os.environ["ENV"] = "test"

import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from tests.testing_database import TestingSessionLocal,engine
from dependencies import get_db
from database import Base
from tests.mocks import mock_send_verification_email



@pytest.fixture
def client():
    with patch(
        "services.auth_service.send_verification_email",
        new=mock_send_verification_email,
    ):
        with TestClient(app) as client:
            yield client

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db