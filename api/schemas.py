from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.utils import prepare_logger

logger = prepare_logger()


class ProjectIn(BaseModel):
    name: str
    description: str | None = None
    date_from: datetime
    date_to: datetime
    area: str

    def create(self, session: Session):
        logger.info(f"Creating new project (name={self.name})")
        #TODO: save to db
        #TODO: return full object


class ProjectOut(ProjectIn):
    created_at: datetime
    updated_at: datetime
