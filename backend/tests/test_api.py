import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test123",
            "full_name": "Test User",
            "org_name": "Test Org",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_user():
    """Test user login"""
    # First register
    client.post(
        "/auth/register",
        json={
            "email": "test2@example.com",
            "password": "test123",
            "full_name": "Test User 2",
            "org_name": "Test Org 2",
        },
    )

    # Then login
    response = client.post(
        "/auth/login", json={"email": "test2@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_twilio_webhook():
    """Test Twilio webhook endpoint"""
    # Mock webhook data
    webhook_data = {
        "recordingUrl": "https://example.com/recording.mp3",
        "callSid": "CA123456789",
        "from": "+1234567890",
        "to": "+0987654321",
        "startTime": "2025-08-30T12:00:00Z",
        "duration": 120,
    }

    response = client.post("/calls/webhook/twilio", json=webhook_data)
    # Will need proper auth headers in real implementation
    assert response.status_code in [200, 401]  # 401 expected without auth


def test_health_check():
    """Test basic API health"""
    response = client.get("/")
    # Should return 404 since we don't have a root endpoint
    # This tests that FastAPI is running
    assert response.status_code == 404
