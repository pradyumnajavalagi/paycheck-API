# tests/test_api.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app, get_db
import models
import auth

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Test Data Setup ---
def setup_test_data():
    """Wipes and populates the test database with fresh data."""
    db = TestingSessionLocal()
    # Clear existing data
    db.query(models.Transaction).delete()
    db.query(models.Bill).delete()
    db.query(models.User).delete()
    db.commit()

    # Create new data
    user1 = models.User(user_id="user_1", name="Pradyumna", hashed_password=auth.get_password_hash("pass123"))
    user2 = models.User(user_id="user_2", name="Nico Robin", hashed_password=auth.get_password_hash("pass456"))
    db.add_all([user1, user2])
    db.commit()
    
    bill1 = models.Bill(bill_id="bill_101", amount=100.0, status="DUE", owner=user1)
    bill2 = models.Bill(bill_id="bill_102", amount=200.0, status="PAID", owner=user1)
    db.add_all([bill1, bill2])
    db.commit()
    db.close()

# --- Auth Tests ---

def test_login_for_access_token():
    """Test successful login and token generation."""
    setup_test_data()
    response = client.post("/login", data={"username": "user_1", "password": "pass123"})
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_login_with_wrong_password():
    """Test login failure with an incorrect password."""
    setup_test_data()
    response = client.post("/login", data={"username": "user_1", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# --- Protected Endpoint Tests ---

def test_get_bills_unauthenticated():
    """Test that accessing a protected route without a token fails."""
    setup_test_data()
    response = client.get("/bills/user_1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_own_bills_authenticated():
    """Test that a logged-in user can fetch their own bills."""
    setup_test_data()
    # Login to get a token
    login_response = client.post("/login", data={"username": "user_1", "password": "pass123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Use the token to access the protected route
    response = client.get("/bills/user_1", headers=headers)
    assert response.status_code == 200
    # User 1 has one DUE bill in the test data
    assert len(response.json()) == 1
    assert response.json()[0]["bill_id"] == "bill_101"

def test_get_bills_for_another_user():
    """Test that a user cannot fetch bills for another user (authorization check)."""
    setup_test_data()
    # Login as user_1
    login_response = client.post("/login", data={"username": "user_1", "password": "pass123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Attempt to access bills for user_2
    response = client.get("/bills/user_2", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Operation not permitted"