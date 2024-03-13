import random

import pytest
from fastapi.testclient import TestClient

import db.models as models
from api.main import app
from config.env import API_AUTH_TOKEN
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
    "X-API-KEY": API_AUTH_TOKEN,
}


def test_root():
    response = client.get("/projects/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to 'projects' API."}


def test_unauthorized_request():
    response = client.get("/projects/")
    assert response.status_code == 400
    assert response.json()["detail"] == "X-API-KEY header not provided"


def test_invalid_auth_token():
    response = client.get("/projects/", headers={"X-API-KEY": "Invalid-token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid X-API-KEY"


@pytest.mark.order("first")
@pytest.mark.parametrize("project", VALID_PROJECTS)
def test_create_project_valid(project):
    response = client.post("/projects/create", json=project, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == project["name"]


@pytest.mark.order("second")
def test_save_new_projects(db):
    projects = db.query(models.Project).order_by(models.Project.created_at).all()
    assert len(projects) == N_PROJECTS
    assert projects[0].name == "project_1"


@pytest.mark.parametrize("project", INVALID_PROJECTS)
def test_create_project_invalid(project, db):
    count_before = db.query(models.Project).order_by(models.Project.created_at).count()
    response = client.post("/projects/create", json=project, headers=headers)
    count_after = db.query(models.Project).order_by(models.Project.created_at).count()
    assert response.status_code == 422
    assert count_before == count_after


@pytest.mark.parametrize("project", INVALID_GEOJSON_PROJECTS)
def test_create_project_invalid_geojson(project, db):
    count_before = db.query(models.Project).order_by(models.Project.created_at).count()
    response = client.post("/projects/create", json=project, headers=headers)
    count_after = db.query(models.Project).order_by(models.Project.created_at).count()
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Invalid geojson."
    assert count_before == count_after


@pytest.mark.parametrize("project_id", random.sample(range(1, N_PROJECTS + 1), 5))
def test_read_existing_project(project_id):
    response = client.get(f"/projects/read/{project_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == f"project_{project_id}"


@pytest.mark.parametrize(
    "project_id", random.sample(range(N_PROJECTS + 1, N_PROJECTS + 20), 5)
)
def test_read_nonexistent_project(project_id):
    response = client.get(f"/projects/read/{project_id}", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Project (id={project_id}) not found"


def test_list_projects(db):
    projects_count = (
        db.query(models.Project).order_by(models.Project.created_at).count()
    )
    response = client.get("/projects/list", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == projects_count
    assert response.json()[0]["name"] == "project_1"


@pytest.mark.order("last")
@pytest.mark.parametrize("project_id", random.sample(range(1, N_PROJECTS + 1), 5))
def test_delete_project(project_id, db):
    assert db.query(models.Project).filter(models.Project.id == project_id).first()
    response = client.delete(f"/projects/delete/{project_id}", headers=headers)
    assert response.status_code == 200
    assert not db.query(models.Project).filter(models.Project.id == project_id).first()


@pytest.mark.parametrize("project_id", random.sample(range(1, N_PROJECTS + 1), 5))
def test_update_existing_project(project_id, db):
    response = client.patch(
        f"/projects/update/{project_id}",
        json={"name": f"project_{project_id}_updated"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == f"project_{project_id}_updated"
    db_project = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )
    assert db_project.name == f"project_{project_id}_updated"


@pytest.mark.parametrize(
    "project_id", random.sample(range(N_PROJECTS + 1, N_PROJECTS + 20), 5)
)
def test_update_nonexistent_project(project_id):
    response = client.patch(
        f"/projects/update/{project_id}",
        json={"name": f"project_{project_id}_updated"},
        headers=headers,
    )
    assert response.status_code == 404
