from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete
from datetime import datetime, timedelta
from fastapi import Depends, status
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

inland_transport_view = select(
        models.InlandTransport.id.label("id"),
        models.InlandTransport.cost.label("cost"),

        models.Source.id.label("source_id"),
        models.Source.state.label("source_state"),
        models.Source.city.label("source_city"),
        models.Source.address.label("source_address"),
        models.Source.zipcode.label("source_zipcode"),
        
        models.Destination.id.label("destination_id"),
        models.Destination.state.label("destination_state"),
        models.Destination.zipcode.label("destination_zipcode")
        ).join(models.Source, models.InlandTransport.source_id==models.Source.id
        ).join(models.Destination, models.InlandTransport.destination_id==models.Destination.id)

async def create_inland_transport(data: schemas.InlandTransportCreate, db: Session) -> schemas.InlandTransport:
    try:
        stmt = insert(models.InlandTransport).values(**data.model_dump()).returning(models.InlandTransport.id)
        inserted_inland_transport_id = db.execute(stmt).scalars().first()
        db.commit()
        return await get_inland_transport_by_id(inserted_inland_transport_id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

async def update_inland_transport(id: int, data: schemas.InlandTransportUpdate, db: Session) -> schemas.InlandTransport:
    try:
        values: dict = data.model_dump(exclude_none=True, exclude_unset=True)
        if values == {}:
            return await get_inland_transport_by_id(id, db)
        stmt = update(models.InlandTransport).values(**values).where(models.InlandTransport.id==id).returning(models.InlandTransport)
        source = db.execute(stmt).scalars().first()
        if source is None:
            raise exceptions.ResourceNotFound("Inland transport")
        db.commit()
        return await get_inland_transport_by_id(id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

async def delete_inland_transport(id: int, db: Session) -> None:
    stmt = delete(models.InlandTransport).where(models.InlandTransport.id==id).returning(models.InlandTransport)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Inland transport") 
    db.commit()

async def get_inland_transport_by_id(id: int, db: Session) -> schemas.InlandTransport:
    stmt = inland_transport_view.filter(models.InlandTransport.id==id)
    source = db.execute(stmt).mappings().first()
    if source is None:
        raise exceptions.ResourceNotFound("Inland transport") 
    print(dict(source))
    return schemas.InlandTransport.model_validate(source)

# async def get_inland_transport_by_zipcode(zipcode: str, db: Session) -> schemas.InlandTransport:
#     stmt = select(models.InlandTransport).filter(models.InlandTransport. zipcode==zipcode)
#     source = db.execute(stmt).scalars().first()
#     if source is None:
#         raise exceptions.InlandTransportNotFound()
#     return schemas.InlandTransport.model_validate(source)

async def get_inland_transports(db: Session, page: int = 1, limit: int = 10) -> list[schemas.InlandTransport]:
    stmt = inland_transport_view
    sources = [schemas.InlandTransport.model_validate(source) for source in db.execute(stmt).mappings().all()]
    return sources
