from fastapi import status
from sqlalchemy import select

from models.database_models import Todo


def test_read_all_authenticated(client_admin, todo):
    response = client_admin.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "complete": todo.complete,
            "owner_id": todo.owner_id,
        },
    ]


def test_read_one_authenticated(client_admin, todo):
    response = client_admin.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "priority": todo.priority,
        "complete": todo.complete,
        "owner_id": todo.owner_id,
    }


def test_read_one_authenticated_not_found(client_admin):
    response = client_admin.get("/todo/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_todo_authenticated(client_admin, todo, db):
    request = {
        "title": "test",
        "description": "test",
        "priority": 1,
        "complete": False,
    }
    response = client_admin.post("/todo/create", json=request)
    assert response.status_code == status.HTTP_201_CREATED
    model = db.scalar(select(Todo).where(Todo.id == 2))  # noqa: PLR2004
    assert model.title == request["title"]
    assert model.description == request["description"]
    assert model.priority == request["priority"]
    assert model.complete == request["complete"]
    assert model.owner_id == 1


def test_update_todo_authenticated(client_admin, todo, db):
    request = {
        "title": "updated test",
        "description": "updated test",
        "priority": 4,
        "complete": True,
    }
    response = client_admin.put("/todo/update/1", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    model = db.scalar(select(Todo).where(Todo.id == 1))
    assert model.title == request["title"]
    assert model.description == request["description"]
    assert model.priority == request["priority"]
    assert model.complete == request["complete"]
    assert model.owner_id == 1


def test_delete_todo_authenticated(client_admin, todo, db):
    response = client_admin.delete("/todo/delete/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    model = db.scalar(select(Todo).where(Todo.id == 1))
    assert model is None


def test_read_all_not_authenticated(client_non_user, todo):
    response = client_non_user.get("/todo")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }


def test_read_one_not_authenticated(client_non_user, todo):
    response = client_non_user.get("/todo/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }


def test_create_todo_not_authenticated(client_non_user, todo):
    request = {
        "title": "test",
        "description": "test",
        "priority": 1,
        "complete": False,
    }
    response = client_non_user.post("/todo/create", json=request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }


def test_update_todo_not_authenticated(client_non_user, todo):
    request = {
        "title": "updated test",
        "description": "updated test",
        "priority": 4,
        "complete": True,
    }
    response = client_non_user.put("/todo/update/1", json=request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }


def test_delete_todo_not_authenticated(client_non_user, todo):
    response = client_non_user.delete("/todo/delete/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }
