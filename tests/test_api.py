from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.main import app

# Utilisation de TestClient pour tester l'application FastAPI
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {'message': 'Hello World'}
