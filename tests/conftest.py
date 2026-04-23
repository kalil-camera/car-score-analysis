"""
Pytest configuration and fixtures
"""
import os
import pytest
from typing import Generator


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Get test database URL from environment or use default"""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://admin:testpass123@localhost:5432/pythonapp"
    )


@pytest.fixture
def mock_sqs_queue():
    """Mock SQS queue for testing"""
    return {
        "url": "https://sqs.us-east-1.amazonaws.com/123456789/pythonbackend-queue",
        "arn": "arn:aws:sqs:us-east-1:123456789:pythonbackend-queue",
    }


@pytest.fixture
def mock_environment():
    """Set up mock environment variables"""
    env_vars = {
        "AWS_REGION": "us-east-1",
        "ENVIRONMENT": "test",
        "DATABASE_URL": "postgresql://admin:testpass123@localhost:5432/pythonapp",
    }
    
    old_environ = os.environ.copy()
    os.environ.update(env_vars)
    
    yield env_vars
    
    os.environ.clear()
    os.environ.update(old_environ)
