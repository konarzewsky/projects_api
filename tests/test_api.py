import pytest
from fastapi.testclient import TestClient

from api.main import app
from tests.data import INVALID_GEOJSON_PROJECTS, INVALID_PROJECTS, VALID_PROJECTS

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


# TODO: add auth token test


@pytest.mark.parametrize("project", VALID_PROJECTS)
def test_create_project_valid(project):
    response = client.post("/create", json=project, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == project["name"]


@pytest.mark.parametrize("project", INVALID_PROJECTS)
def test_create_project_invalid(project):
    response = client.post("/create", json=project, headers=headers)
    assert response.status_code == 422


@pytest.mark.parametrize("project", INVALID_GEOJSON_PROJECTS)
def test_create_project_invalid_geojson(project):
    response = client.post("/create", json=project, headers=headers)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Invalid geojson."
