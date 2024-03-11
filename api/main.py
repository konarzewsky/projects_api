from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.dependencies import get_db_conn
from api.schemas import ProjectIn, ProjectOut

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to 'projects' API."}


@app.post("/create", response_model=ProjectOut)
async def add_date(project: ProjectIn, session: Session = Depends(get_db_conn)):
    # TODO: add input validation
    return project.create(session=session)
