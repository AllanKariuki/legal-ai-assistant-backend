import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from alembic.config import Config
from alembic import command

# Add the parent directory to path so we can import the app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import Base, get_db
from app.models.database import User, Conversation, Message
from main import app

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_migrations():
    """Run migrations to create all tables in the test database"""
    # Get the path to the alembic configuration file
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    
    # Set the path to the migrations directory
    alembic_cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "migrations"))
    
    # Set the SQLAlchemy URL to the test database
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    
    # Run the migrations
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database once for all tests"""
    # Create fresh database tables using migrations
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    run_migrations()
    yield
    # Clean up after all tests
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def test_db():
    # Database tables are already created by the migrations
    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # No need to drop tables after each test, we'll clean the specific data instead
        db.execute("DELETE FROM messages")
        db.execute("DELETE FROM conversations")
        db.execute("DELETE FROM users")
        db.commit()

@pytest.fixture(scope="function")
def client(test_db):
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a test client
    with TestClient(app) as c:
        yield c
    
    # Reset the dependency override
    app.dependency_overrides = {}

@pytest.fixture
def mock_llm_response(monkeypatch):
    # Mock the LLM service to return a predefined response
    async def mock_get_llm_response(query):
        return f"This is a mock response to: {query}"
    
    from app.services import llm_service
    monkeypatch.setattr(llm_service, "get_llm_response", mock_get_llm_response)