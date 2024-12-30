import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db, Base
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Database session for testing"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db  # Provide the database session to the tests
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)

# Define client fixture
@pytest.fixture(scope="function")
def client(db_session):
    """Client fixture with overridden get_db dependency"""
    # Override the dependency to use test db_session
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client