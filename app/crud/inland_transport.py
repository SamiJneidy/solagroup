from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_
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
        
        models.Warehouse.id.label("warehouse_id"),
        models.Warehouse.state.label("warehouse_state"),
        models.Warehouse.zipcode.label("warehouse_zipcode")
        ).join(models.Source, models.InlandTransport.source_id==models.Source.id
        ).join(models.Warehouse, models.InlandTransport.warehouse_id==models.Warehouse.id)

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
        inland_transport = db.execute(stmt).scalars().first()
        if inland_transport is None:
            raise exceptions.ResourceNotFound("Inland transport")
        db.commit()
        return await get_inland_transport_by_id(id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

async def delete_inland_transport(id: int, db: Session) -> None:
    stmt = delete(models.InlandTransport).where(models.InlandTransport.id==id).returning(models.InlandTransport)
    inland_transport = db.execute(stmt).scalars().first()
    if inland_transport is None:
        raise exceptions.ResourceNotFound("Inland transport") 
    db.commit()

async def get_inland_transport_by_id(id: int, db: Session) -> schemas.InlandTransport:
    stmt = inland_transport_view.filter(models.InlandTransport.id==id)
    inland_transport = db.execute(stmt).mappings().first()
    if inland_transport is None:
        raise exceptions.ResourceNotFound("Inland transport") 
    return schemas.InlandTransport.model_validate(inland_transport)

async def get_inland_transports(db: Session, page: int = 1, limit: int = 10) -> schemas.Pagination[schemas.InlandTransport]:
    stmt = inland_transport_view.offset((page-1)*limit).limit(limit)
    data = [schemas.InlandTransport.model_validate(inland_transport) for inland_transport in db.execute(stmt).mappings().all()]
    total_rows = db.execute(select(func.count(models.InlandTransport.id))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.InlandTransport](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response


async def get_inland_transport_between(source_id: int, warehouse_id: int, db: Session) -> float:
    cost = db.execute(
        select(models.InlandTransport.cost).where(and_(
            models.InlandTransport.source_id==source_id,
            models.InlandTransport.warehouse_id==warehouse_id,
            )
        )
    ).scalar()
    if cost is None:
        raise exceptions.ResourceNotFound("Inland Transport")
    return cost