from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends, status
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models, utils

maritime_transport_view = select(
        models.MaritimeTransport.id.label("id"),
        models.MaritimeTransport.cost.label("cost"),

        models.ShippingLine.id.label("shipping_line_id"),
        models.ShippingLine.name.label("shipping_line_name"),
        
        models.Warehouse.id.label("warehouse_id"),
        models.Warehouse.state.label("warehouse_state"),
        models.Warehouse.zipcode.label("warehouse_zipcode"),

        models.Destination.id.label("destination_id"),
        models.Destination.country.label("destination_country"),
        models.Destination.port.label("destination_port"),

        ).join(models.ShippingLine, models.MaritimeTransport.shipping_line_id==models.ShippingLine.id
        ).join(models.Warehouse, models.MaritimeTransport.warehouse_id==models.Warehouse.id
        ).join(models.Destination, models.MaritimeTransport.destination_id==models.Destination.id)

async def create_maritime_transport(data: schemas.MaritimeTransportCreate, db: Session) -> schemas.MaritimeTransport:
    try:
        stmt = insert(models.MaritimeTransport).values(**data.model_dump()).returning(models.MaritimeTransport.id)
        inserted_maritime_transport_id = db.execute(stmt).scalars().first()
        db.commit()
        return await get_maritime_transport_by_id(inserted_maritime_transport_id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)        
        raise exceptions.classify_foreign_key_violation(error_message, "Maritime transport")

async def update_maritime_transport(id: int, data: schemas.MaritimeTransportUpdate, db: Session) -> schemas.MaritimeTransport:
    try:
        values: dict = data.model_dump(exclude_unset=True)
        if values == {}:
            return await get_maritime_transport_by_id(id, db)
        stmt = update(models.MaritimeTransport).values(**values).where(models.MaritimeTransport.id==id).returning(models.MaritimeTransport)
        maritime_transport = db.execute(stmt).scalars().first()
        if maritime_transport is None:
            raise exceptions.ResourceNotFound(resource="Maritime transport")
        db.commit()
        return await get_maritime_transport_by_id(id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.classify_foreign_key_violation(error_message, "Maritime transport")

async def delete_maritime_transport(id: int, db: Session) -> None:
    stmt = delete(models.MaritimeTransport).where(models.MaritimeTransport.id==id).returning(models.MaritimeTransport)
    maritime_transport = db.execute(stmt).scalars().first()
    if maritime_transport is None:
        raise exceptions.ResourceNotFound(resource="Maritime transport") 
    db.commit()

async def get_maritime_transport_by_id(id: int, db: Session) -> schemas.MaritimeTransport:
    stmt = maritime_transport_view.filter(models.MaritimeTransport.id==id)
    maritime_transport = db.execute(stmt).mappings().first()
    if maritime_transport is None:
        raise exceptions.ResourceNotFound(resource="Maritime transport") 
    return schemas.MaritimeTransport.model_validate(maritime_transport)

async def get_maritime_transports(db: Session, warehouse_id: int, shipping_line_id: int, destination_id: int, page: int, limit: int) -> schemas.Pagination[schemas.MaritimeTransport]:
    where_clause = and_(
        or_(warehouse_id is None, models.MaritimeTransport.warehouse_id==warehouse_id),
        or_(shipping_line_id is None, models.MaritimeTransport.shipping_line_id==shipping_line_id),
        or_(destination_id is None, models.MaritimeTransport.destination_id==destination_id),
    )
    stmt = maritime_transport_view.where(where_clause).order_by(models.Warehouse.state, models.Warehouse.city, models.ShippingLine.name, models.MaritimeTransport.id)
    if page is not None and limit is not None:
        stmt = stmt.offset((page-1)*limit).limit(limit)
    data = [schemas.MaritimeTransport.model_validate(maritime_transport) for maritime_transport in db.execute(stmt).mappings().all()]
    total_rows = db.execute(select(func.count()).select_from(maritime_transport_view.where(where_clause))).scalar()
    total_pages = None if limit is None else (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.MaritimeTransport](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response


async def get_maritime_transport_between(warehouse_id: int, shipping_line_id: int, destination_country: str, destination_port: str, db: Session) -> float:
    from .destination import get_destinations
    destination = await get_destinations(db, destination_country, destination_port, None, None)
    destination_id = destination.data[0].id
    cost = db.execute(
        select(models.MaritimeTransport.cost).where(and_(
            models.MaritimeTransport.shipping_line_id==shipping_line_id,
            models.MaritimeTransport.warehouse_id==warehouse_id,
            models.MaritimeTransport.destination_id==destination_id
            )
        )
    ).scalar()
    if cost is None:
        raise exceptions.ResourceNotFound(resource="Maritime transport")
    return cost