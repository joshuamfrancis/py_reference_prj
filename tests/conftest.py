"""Test configuration and fixtures"""
import pytest
from app import create_app
from app.config import TestingConfig
from app.models import user_store


@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_app(TestingConfig)

    yield app

    # Cleanup
    user_store.clear_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Create application context"""
    with app.app_context():
        yield app
