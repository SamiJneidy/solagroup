from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
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

async def get_sources(db: Session, source_state: str, source_city: str, source_address: str, source_zipcode: str, page: int, limit: int) -> schemas.Pagination[schemas.Source]:
    where_clause = and_(
        or_(source_state is None, func.lower(models.Source.state)==func.lower(source_state)),
        or_(source_city is None, func.lower(models.Source.city)==func.lower(source_city)),
        or_(source_address is None, func.lower(models.Source.address)==func.lower(source_address)),
        or_(source_zipcode is None, func.lower(models.Source.zipcode)==func.lower(source_zipcode))
    ) 
    stmt = select(models.Source).where(where_clause).order_by(models.Source.state, models.Source.city, models.Source.zipcode, models.Source.id).offset((page-1)*limit).limit(limit)
    data = [schemas.Source.model_validate(source) for source in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.Source.id)).where(where_clause)).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.Source](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response
