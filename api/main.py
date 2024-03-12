from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.dependencies import get_db_conn
from api.schemas import BaseProject, Project

app = FastAPI()


@app.get("/projects")
async def root():
    return {"message": "Welcome to 'projects' API."}


@app.post("/projects/create", response_model=Project)
async def create_project(project: BaseProject, session: Session = Depends(get_db_conn)):
    return project.create(session=session)


@app.get("/projects/read/{project_id}", response_model=Project)
async def read_project(project_id: int, session: Session = Depends(get_db_conn)):
    return Project.get(id=project_id, session=session)


@app.get("/projects/list", response_model=list[Project])  # TODO: check return typing
async def list_projects(session: Session = Depends(get_db_conn)):
    return Project.get_all(session=session)


@app.delete("/projects/delete/{project_id}")
async def delete_project(project_id: int, session: Session = Depends(get_db_conn)):
    return Project.delete(id=project_id, session=session)
