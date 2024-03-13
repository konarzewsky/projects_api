import datetime
from typing import Self

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
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
        today = datetime.date.today()
        if self.date_start > today or self.date_start > today:
            raise ValueError("date_start and date_end cannot be in the future")
        if self.date_start > self.date_end:
            raise ValueError("date_start cannot be later than date_end")
        return self

    @field_validator("area")
    @classmethod
    def check_geojson_structure(cls, area: dict) -> dict:
        if not validate_geojson(area):
            raise ValueError("Invalid geojson.")
        return area

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


class ProjectUpdate(BaseModel):
    """
    All fields are optional here to allow updating only chosen fields
    """

    name: str | None = Field(default=None, min_length=1, max_length=32)
    description: str | None = Field(default=None)
    date_start: datetime.date | None = None
    date_end: datetime.date | None = None
    area: dict | None = None

    @model_validator(mode="after")
    def check_dates_chronology(self) -> Self:
        today = datetime.date.today()
        for date in [self.date_start, self.date_end]:
            if date:
                if date > today:
                    raise ValueError("date cannot be in the future")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise ValueError("date_start cannot be later than date_end")
        return self

    @field_validator("area")
    @classmethod
    def check_geojson_structure(cls, area: dict) -> dict:
        if area:
            if not validate_geojson(area):
                raise ValueError("Invalid geojson.")
        return area

    def update(self, id: int, session: Session) -> models.Project:
        logger.info(f"Updating project (id={id})")
        db_project = session.query(models.Project).filter_by(id=id).first()
        if not db_project:
            raise HTTPException(status_code=404, detail=f"Project (id={id}) not found")
        for k, v in self.model_dump(exclude_unset=True).items():
            setattr(db_project, k, v)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        return db_project


class Project(BaseProject):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @staticmethod
    def get(id: int, session: Session) -> models.Project:
        logger.info(f"Getting project (id={id})")
        db_project = (
            session.query(models.Project).filter(models.Project.id == id).first()
        )
        if db_project is None:
            raise HTTPException(status_code=400, detail=f"Project (id={id}) not found")
        return db_project

    @staticmethod
    def get_all(session: Session) -> list[models.Project]:
        logger.info("Getting all projects")
        return session.query(models.Project).order_by(models.Project.id).all()

    @staticmethod
    def delete(id: int, session: Session) -> dict:
        logger.info(f"Deleting project with id={id}")
        project = session.get(models.Project, id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project (id={id}) not found")
        try:
            session.delete(project)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=e)
        else:
            return {"detail": f"Project (id={id}) deleted"}
