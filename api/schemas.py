import datetime
from typing import Self

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import db.models as models
from api.utils import prepare_logger, validate_geojson

logger = prepare_logger()


class BaseProject(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    description: str | None = Field(default=None)
    date_start: datetime.date
    date_end: datetime.date
    area: dict

    @model_validator(mode="after")
    def check_dates_chronology(self) -> Self:
        if self.date_start > self.date_end:
            raise ValueError("date_start cannot be later than date_end")
        return self

    @field_validator("area")
    @classmethod
    def check_geojson_structure(cls, v: dict) -> dict:
        if not validate_geojson(v):
            raise ValueError("Invalid geojson.")
        return v

    def create(self, session: Session) -> models.Project:
        logger.info(f"Creating new project (name={self.name})")
        project = models.Project(
            name=self.name,
            description=self.description,
            date_start=self.date_start,
            date_end=self.date_end,
            area=self.area,
        )
        try:
            session.add(project)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=e)
        else:
            return project


class Project(BaseProject):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

    @staticmethod
    def get(id: int, session: Session) -> models.Project:
        logger.info(f"Getting project (id={id})")
        db_project = (
            session.query(models.Project).filter(models.Project.id == id).first()
        )
        if db_project is None:
            raise HTTPException(
                status_code=400, detail=f"Project with id={id} not found"
            )
        return db_project

    @staticmethod
    def get_all(session: Session) -> list[models.Project]:
        logger.info("Getting all projects")
        return session.query(models.Project).order_by(models.Project.id).all()
