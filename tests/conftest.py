import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities

# Store original activities for restoration
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Provide a TestClient instance"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test (Arrange)"""
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
