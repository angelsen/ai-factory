from fastapi.testclient import TestClient
import pytest
import json
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "AI Factory API" in response.json()["message"]

# Add more tests for your API endpoints here
# For example:
# def test_list_functions():
#     response = client.get("/api/admin/functions")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)