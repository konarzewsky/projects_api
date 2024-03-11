from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.dependencies import get_db_conn
from api.schemas import BaseProject, Project

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to 'projects' API."}


@app.post("/create")
async def add_date(
    project: BaseProject, session: Session = Depends(get_db_conn)
) -> Project:
    return project.create(session=session)
