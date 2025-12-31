import pytest
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def test_settings():
    """Provide test settings."""
    return {
        "database_url": "postgresql://test:test@localhost:5432/test_db",
        "redis_url": "redis://localhost:6379/0",
        "secret_key": "test-secret-key-for-testing-only",
        "environment": "test"
    }
