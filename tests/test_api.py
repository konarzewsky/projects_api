import random

import pytest
from fastapi.testclient import TestClient

import db.models as models
from api.main import app
from tests.data import (
    INVALID_GEOJSON_PROJECTS,
    INVALID_PROJECTS,
    N_PROJECTS,
    VALID_PROJECTS,
)

pytest_plugins = ["tests.fixtures"]

client = TestClient(app)


headers = {
    "Content-Type": "application/json;charset=UTF-8",
    # "X-API-KEY": API_AUTH_TOKEN,
}


def test_root():
    response = client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to 'projects' API."}


# TODO: add auth token test


@pytest.mark.parametrize("project", VALID_PROJECTS)
def test_create_project_valid(project):
    response = client.post("/projects/create", json=project, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == project["name"]


def test_save_new_projects(db):
    projects = db.query(models.Project).order_by(models.Project.created_at).all()
    assert len(projects) == N_PROJECTS
    assert projects[0].name == "project_1"


@pytest.mark.parametrize("project", INVALID_PROJECTS)
def test_create_project_invalid(project):
    response = client.post("/projects/create", json=project, headers=headers)
    assert response.status_code == 422


@pytest.mark.parametrize("project", INVALID_GEOJSON_PROJECTS)
def test_create_project_invalid_geojson(project):
    response = client.post("/projects/create", json=project, headers=headers)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Invalid geojson."


@pytest.mark.parametrize("project_id", random.sample(range(1, N_PROJECTS + 1), 5))
def test_read_existing_project(project_id):
    response = client.get(f"/projects/read/{project_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == f"project_{project_id}"
