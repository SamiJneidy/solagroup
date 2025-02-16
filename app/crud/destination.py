from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete
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
        raise exceptions.ZipCodeAlreadyInUse()

async def update_destination(id: int, data: schemas.DestinationUpdate, db: Session) -> schemas.Destination:
    try:
        values: dict = data.model_dump(exclude_none=True, exclude_unset=True)
        if values == {}:
            return await get_destination_by_id(id, db)
        stmt = update(models.Destination).values(**values).where(models.Destination.id==id).returning(models.Destination)
        destination = db.execute(stmt).scalars().first()
        if destination is None:
            raise exceptions.DestinationNotFound()
        db.commit()
        return schemas.Destination.model_validate(destination)   
    except IntegrityError:
        raise exceptions.ZipCodeAlreadyInUse()

async def delete_destination(id: int, db: Session) -> None:
    try:
        stmt = delete(models.Destination).where(models.Destination.id==id).returning(models.Destination)
        destination = db.execute(stmt).scalars().first()
        if destination is None:
            raise exceptions.DestinationNotFound()  
        db.commit()
    except IntegrityError:
        raise exceptions.ZipCodeAlreadyInUse()

async def get_destination_by_id(id: int, db: Session) -> schemas.Destination:
    stmt = select(models.Destination).filter(models.Destination.id==id)
    destination = db.execute(stmt).scalars().first()
    if destination is None:
        raise exceptions.DestinationNotFound()
    return schemas.Destination.model_validate(destination)

async def get_destination_by_zipcode(zipcode: str, db: Session) -> schemas.Destination:
    stmt = select(models.Destination).filter(models.Destination.zipcode==zipcode)
    destination = db.execute(stmt).scalars().first()
    if destination is None:
        raise exceptions.DestinationNotFound()
    return schemas.Destination.model_validate(destination)

async def get_destinations(db: Session, page: int = 1, limit: int = 10) -> list[schemas.Destination]:
    stmt = select(models.Destination).offset((page-1)*limit).limit(limit)
    destinations = [schemas.Destination.model_validate(destination) for destination in db.execute(stmt).scalars().all()]
    return destinations