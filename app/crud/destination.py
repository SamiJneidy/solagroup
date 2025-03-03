from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def create_destination(data: schemas.DestinationCreate, db: Session) -> schemas.Destination:
    try:
        stmt = insert(models.Destination).values(**data.model_dump()).returning(models.Destination)
        inserted_destination = db.execute(stmt).scalars().first()
        db.commit()
        return schemas.Destination.model_validate(inserted_destination)
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse(resource="Destination")

async def update_destination(id: int, data: schemas.DestinationUpdate, db: Session) -> schemas.Destination:
    try:
        values: dict = data.model_dump(exclude_unset=True)
        if values == {}:
            return await get_destination_by_id(id, db)
        stmt = update(models.Destination).values(**values).where(models.Destination.id==id).returning(models.Destination)
        destination = db.execute(stmt).scalars().first()
        if destination is None:
            raise exceptions.ResourceNotFound(resource="Destination")
        db.commit()
        return schemas.Destination.model_validate(destination)   
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse(resource="Destination")

async def delete_destination(id: int, db: Session) -> None:
    try:
        stmt = delete(models.Destination).where(models.Destination.id==id).returning(models.Destination)
        destination = db.execute(stmt).scalars().first()
        if destination is None:
            raise exceptions.ResourceNotFound(resource="Destination") 
        db.commit()
    except IntegrityError:
        raise exceptions.ForeignKeyConstraintViolation()

async def get_destination_by_id(id: int, db: Session) -> schemas.Destination:
    stmt = select(models.Destination).filter(models.Destination.id==id)
    destination = db.execute(stmt).scalars().first()
    if destination is None:
        raise exceptions.ResourceNotFound(resource="Destination") 
    return schemas.Destination.model_validate(destination)

async def get_destinations(db: Session, country: str, port: str, page: int, limit: int) -> schemas.Pagination[schemas.Destination]:
    where_clause = and_(
        or_(country is None, models.Destination.country==country),
        or_(port is None, models.Destination.port==port)
    )
    stmt = select(models.Destination).where(where_clause).order_by(models.Destination.country, models.Destination.port, models.Destination.id)
    if page is not None and limit is not None:
        stmt = stmt.offset((page-1)*limit).limit(limit)
    data = [schemas.Destination.model_validate(destination) for destination in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.Destination.id)).where(where_clause)).scalar()
    total_pages = None if limit is None else (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.Destination](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response
