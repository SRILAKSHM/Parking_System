import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import based on your project structure
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import user_model
# tests/test_add_user.py

# Create a test database engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db function to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply overrides to FastAPI app
app.dependency_overrides[get_db] = override_get_db

# Fixture to reset DB before each test
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Test cases for the add_user endpoint
@pytest.mark.asyncio
def test_add_user():
    client = TestClient(app)
    
    # Test 1: Successful user creation
    payload = {"username": "testuser", "password": "securepassword", "role": "user"}
    response = client.post("/api/Parking_System/add_user", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "User added successfully"
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"
    
    # Test 2: User already exists
    response = client.post("/api/Parking_System/add_user", json=payload)  # Same user again
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    
    # Test 3: Invalid role (neither "admin" nor "user")
    invalid_payload = {"username": "invaliduser", "password": "securepassword", "role": "guest"}
    response = client.post("/api/Parking_System/add_user", json=invalid_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Role must be admin or user"

