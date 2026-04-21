import pytest
from fastapi.testclient import TestClient

from backendapi.app import app


@pytest.fixture
def client():
    return TestClient(app)
