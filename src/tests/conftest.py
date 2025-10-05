import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.app.main import create_application
from src.app.models.database import Base, get_db
from src.app.config import settings

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with override database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app = create_application()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        "session_id": 1,
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 2,
                "unit_price": 5.99,
                "selected_modifiers": {"size": "large"},
                "special_instructions": "No onions"
            }
        ]
    }

@pytest.fixture
def sample_conversation_data():
    """Sample conversation data for testing"""
    return {
        "session_id": 1,
        "speaker": "customer",
        "utterance_text": "I want a cheeseburger and fries",
        "intent": "ordering",
        "track": "ordering"
    }