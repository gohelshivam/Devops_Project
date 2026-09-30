import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test ki homepage HTTP 200 return karta hai aur text verify ho raha hai"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevOps Cloud Application" in response.data

def test_health_check(client):
    """Test ki /health endpoint status healthy aur HTTP 200 return karta hai"""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert "timestamp" in json_data
    assert "version" in json_data

def test_info_endpoint(client):
    """Test ki /api/info metadata theek se return karta hai"""
    response = client.get("/api/info")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["app_name"] == "DevOps Cloud Web Application"
    assert "tech_stack" in json_data
