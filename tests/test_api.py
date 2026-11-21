
import pytest

from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):

    test_database = tmp_path / "test_tasks.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database
    )

    with TestClient(app) as test_client:
        yield test_client


def test_home(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["status"] == "Running"


def test_create_task(client):

    response = client.post(
        "/tasks",
        json={
            "title": "Complete Python API",
            "description": "Build SWYNEX project",
            "status": "pending"
        }
    )

    assert response.status_code == 201

    assert response.json()["title"] == "Complete Python API"


def test_get_all_tasks(client):

    client.post(
        "/tasks",
        json={"title": "First task"}
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    assert len(response.json()) == 1


def test_get_task_by_id(client):

    created = client.post(
        "/tasks",
        json={"title": "Testing API"}
    )

    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    assert response.json()["title"] == "Testing API"


def test_update_task(client):

    created = client.post(
        "/tasks",
        json={"title": "Old title"}
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "completed"}
    )

    assert response.status_code == 200

    assert response.json()["status"] == "completed"


def test_delete_task(client):

    created = client.post(
        "/tasks",
        json={"title": "Delete me"}
    )

    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    check = client.get(f"/tasks/{task_id}")

    assert check.status_code == 404


def test_invalid_task(client):

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "status": "unknown"
        }
    )

    assert response.status_code == 422


def test_missing_task(client):

    response = client.get("/tasks/9999")

    assert response.status_code == 404
