from flask import Flask
from app import create_app, db
from app.models import Data
import pytest


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_insert_data(client):
    response = client.post(
        "/data",
        json={"name": "John Doe"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Data.query.count() == 1
    assert Data.query.first().name == "John Doe"


def test_insert_duplicate_data(client):
    client.post("/data", json={"name": "Jane Doe"}, content_type="application/json")
    response = client.post(
        "/data",
        json={"name": "Jane Doe"},
        content_type="application/json",
    )
    assert response.status_code == 409
    assert Data.query.count() == 1


def test_get_all_data(client):
    client.post("/data", json={"name": "Alice"}, content_type="application/json")
    client.post("/data", json={"name": "Bob"}, content_type="application/json")

    response = client.get("/data")
    assert response.status_code == 200
    data_list = response.get_json()
    assert len(data_list) == 2
    assert {"id": 1, "name": "Alice"} in data_list
    assert {"id": 2, "name": "Bob"} in data_list


def test_delete_data(client):
    client.post("/data", json={"name": "Charlie"}, content_type="application/json")

    response = client.delete("/data/1")
    assert response.status_code == 200
    assert Data.query.count() == 0


def test_delete_nonexistent_data(client):
    response = client.delete("/data/1")
    assert response.status_code == 404
    assert Data.query.count() == 0
