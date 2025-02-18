from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def create_source(data: schemas.SourceCreate, db: Session) -> schemas.Source:
    try:
        stmt = insert(models.Source).values(**data.model_dump()).returning(models.Source)
        inserted_source = db.execute(stmt).scalars().first()
        db.commit()
        return schemas.Source.model_validate(inserted_source)
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse("Zipcode")

async def update_source(id: int, data: schemas.SourceUpdate, db: Session) -> schemas.Source:
    try:
        values: dict = data.model_dump(exclude_none=True, exclude_unset=True)
        if values == {}:
            return await get_source_by_id(id, db)
        stmt = update(models.Source).values(**values).where(models.Source.id==id).returning(models.Source)
        source = db.execute(stmt).scalars().first()
        if source is None:
            raise exceptions.ResourceNotFound("Source")
        db.commit()
        return schemas.Source.model_validate(source)   
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse("Zipcode")

async def delete_source(id: int, db: Session) -> None:
    stmt = delete(models.Source).where(models.Source.id==id).returning(models.Source)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Source") 
    db.commit()

async def get_source_by_id(id: int, db: Session) -> schemas.Source:
    stmt = select(models.Source).filter(models.Source.id==id)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Source") 
    return schemas.Source.model_validate(source)

async def get_source_by_zipcode(zipcode: str, db: Session) -> schemas.Source:
    stmt = select(models.Source).filter(models.Source.zipcode==zipcode)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Source") 
    return schemas.Source.model_validate(source)

async def get_sources(db: Session, page: int = 1, limit: int = 10) -> list[schemas.Source]:
    stmt = select(models.Source).offset((page-1)*limit).limit(limit)
    sources = [schemas.Source.model_validate(source) for source in db.execute(stmt).scalars().all()]
    return sources
