import pytest
from app import create_app
from extensions import db
from models import Task


@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    with app.test_client() as c:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield c
        with app.app_context():
            db.drop_all()


def test_list_empty(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.get_json()["items"] == []
    assert r.get_json()["total"] == 0


def test_create_task(client):
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    body = r.get_json()
    assert body["title"] == "Buy milk"
    assert body["done"] is False
    assert "id" in body


def test_create_invalid_task(client):
    r = client.post("/tasks", json={})
    assert r.status_code == 400
    assert "title" in r.get_json()


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old"}).get_json()
    r = client.put(f"/tasks/{created['id']}", json={"title": "New", "done": True})
    assert r.status_code == 200
    body = r.get_json()
    assert body["title"] == "New"
    assert body["done"] is True


def test_update_missing_task(client):
    r = client.put("/tasks/9999", json={"title": "X"})
    assert r.status_code == 404


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Temp"}).get_json()
    r = client.delete(f"/tasks/{created['id']}")
    assert r.status_code == 204
    assert client.get("/tasks").get_json()["total"] == 0


def test_pagination(client):
    for i in range(15):
        client.post("/tasks", json={"title": f"task {i}"})
    r = client.get("/tasks?page=1&per_page=10")
    body = r.get_json()
    assert len(body["items"]) == 10
    assert body["total"] == 15
    assert body["pages"] == 2
    r2 = client.get("/tasks?page=2&per_page=10")
    assert len(r2.get_json()["items"]) == 5