import pytest
from src.config import get_settings
from src.db.interfaces.postgresql import PostgreSQLDatabase

@pytest.fixture(scope="session")
def settings():
    return get_settings()

@pytest.fixture(scope="session")
def db(settings):
    db = PostgreSQLDatabase(settings)
    db.startup()
    yield db
    db.teardown()
    
@pytest.fixture(scope="function")
def session(db):
    """Fresh db session for each test"""
    with db.get_session() as session:
        yield session