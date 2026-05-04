from fastapi.testclient import TestClient

def test_create_url(client: TestClient):
    response = client.post("/urls/", json={"original_url": "https://youtube.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["original_url"] == "https://youtube.com/"
    assert "short_code" in data
    assert data["clicks"] == 0

def test_read_urls(client: TestClient):
    client.post("/urls/", json={"original_url": "https://youtube.com"})
    client.post("/urls/", json={"original_url": "https://github.com"})

    response = client.get("/urls/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_url(client: TestClient):
    create = client.post("/urls/", json={"original_url": "https://youtube.com"})
    short_code = create.json()["short_code"]

    response = client.get(f"/urls/{short_code}")
    assert response.status_code == 200
    assert response.json()["short_code"] == short_code

def test_read_url_not_found(client: TestClient):
    response = client.get("/urls/doesnotexist")
    assert response.status_code == 404

def test_update_url(client: TestClient):
    create = client.post("/urls/", json={"original_url": "https://youtube.com"})
    short_code = create.json()["short_code"]

    response = client.patch(f"/urls/{short_code}", json={"original_url": "https://github.com"})
    assert response.status_code == 200
    assert response.json()["original_url"] == "https://github.com/"

def test_delete_url(client: TestClient):
    create = client.post("/urls/", json={"original_url": "https://youtube.com"})
    short_code = create.json()["short_code"]

    response = client.delete(f"/urls/{short_code}")
    assert response.status_code == 200

    response = client.get(f"/urls/{short_code}")
    assert response.status_code == 404