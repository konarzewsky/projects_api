from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.dependencies import get_db_conn
from api.schemas import BaseProject, Project

app = FastAPI()


@app.get("/projects")
async def root():
    return {"message": "Welcome to 'projects' API."}


@app.post("/projects/create")
async def create_project(
    project: BaseProject, session: Session = Depends(get_db_conn)
) -> Project:
    return project.create(session=session)


@app.get("/projects/read/{project_id}")
async def read_project(
    project_id: int, session: Session = Depends(get_db_conn)
) -> Project:
    return Project.get(id=project_id, session=session)
