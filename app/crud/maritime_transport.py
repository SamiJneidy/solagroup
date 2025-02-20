from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func
from datetime import datetime, timedelta
from fastapi import Depends, status
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

maritime_transport_view = select(
        models.MaritimeTransport.id.label("id"),
        models.MaritimeTransport.cost.label("cost"),

        models.ShippingLine.id.label("shipping_line_id"),
        models.ShippingLine.name.label("shipping_line_name"),
        
        models.Warehouse.id.label("warehouse_id"),
        models.Warehouse.state.label("warehouse_state"),
        models.Warehouse.zipcode.label("warehouse_zipcode")
        ).join(models.ShippingLine, models.MaritimeTransport.shipping_line_id==models.ShippingLine.id
        ).join(models.Warehouse, models.MaritimeTransport.warehouse_id==models.Warehouse.id)

async def create_maritime_transport(data: schemas.MaritimeTransportCreate, db: Session) -> schemas.MaritimeTransport:
    try:
        stmt = insert(models.MaritimeTransport).values(**data.model_dump()).returning(models.MaritimeTransport.id)
        inserted_maritime_transport_id = db.execute(stmt).scalars().first()
        db.commit()
        return await get_maritime_transport_by_id(inserted_maritime_transport_id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

async def update_maritime_transport(id: int, data: schemas.MaritimeTransportUpdate, db: Session) -> schemas.MaritimeTransport:
    try:
        values: dict = data.model_dump(exclude_none=True, exclude_unset=True)
        if values == {}:
            return await get_maritime_transport_by_id(id, db)
        stmt = update(models.MaritimeTransport).values(**values).where(models.MaritimeTransport.id==id).returning(models.MaritimeTransport)
        maritime_transport = db.execute(stmt).scalars().first()
        if maritime_transport is None:
            raise exceptions.ResourceNotFound("Maritime transport")
        db.commit()
        return await get_maritime_transport_by_id(id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

async def delete_maritime_transport(id: int, db: Session) -> None:
    stmt = delete(models.MaritimeTransport).where(models.MaritimeTransport.id==id).returning(models.MaritimeTransport)
    maritime_transport = db.execute(stmt).scalars().first()
    if maritime_transport is None:
        raise exceptions.ResourceNotFound("Maritime transport") 
    db.commit()

async def get_maritime_transport_by_id(id: int, db: Session) -> schemas.MaritimeTransport:
    stmt = maritime_transport_view.filter(models.MaritimeTransport.id==id)
    maritime_transport = db.execute(stmt).mappings().first()
    if maritime_transport is None:
        raise exceptions.ResourceNotFound("Maritime transport") 
    return schemas.MaritimeTransport.model_validate(maritime_transport)

async def get_maritime_transports(db: Session, page: int = 1, limit: int = 10) -> schemas.Pagination[schemas.MaritimeTransport]:
    stmt = maritime_transport_view.offset((page-1)*limit).limit(limit)
    data = [schemas.MaritimeTransport.model_validate(maritime_transport) for maritime_transport in db.execute(stmt).mappings().all()]
    total_rows = db.execute(select(func.count(models.MaritimeTransport.id))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.MaritimeTransport](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response
