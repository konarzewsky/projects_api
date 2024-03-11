import pytest
from fastapi.testclient import TestClient

from api.main import app
from tests.data import INVALID_PROJECTS, VALID_PROJECTS

pytest_plugins = ["tests.fixtures"]

client = TestClient(app)


headers = {
    "Content-Type": "application/json;charset=UTF-8",
    # "X-API-KEY": API_AUTH_TOKEN,
}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to 'projects' API."}


@pytest.mark.parametrize("project", VALID_PROJECTS)
def test_create_valid_project(project):
    response = client.post("/create", json=project, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == project["name"]


@pytest.mark.parametrize("project", INVALID_PROJECTS)
def test_create_invalid_project(project):
    response = client.post("/create", json=project, headers=headers)
    assert response.status_code == 422
