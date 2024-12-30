import pytest
from tests.test_setup import client, db_session

@pytest.mark.usefixtures("client")
def test_create_short_url(client):
    response = client.post("/shorten/", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert "long_url" in data
    assert data["long_url"] == "https://example.com"

@pytest.mark.usefixtures("client")
def test_redirect_url(client):
    response = client.post("/shorten/", json={"long_url": "https://example.com"})
    short_url_code = response.json()["short_url"]

    response = client.get(f"/api/{short_url_code}")
    assert response.status_code == 200
    assert response.url == "https://example.com/"

@pytest.mark.usefixtures("client")
def test_redirect_url_not_found(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}