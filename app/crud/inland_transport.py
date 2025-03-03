from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import status
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models, utils

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
        raise exceptions.classify_foreign_key_violation(error_message, "Inland transport")

async def update_inland_transport(id: int, data: schemas.InlandTransportUpdate, db: Session) -> schemas.InlandTransport:
    try:
        values: dict = data.model_dump(exclude_unset=True)
        if values == {}:
            return await get_inland_transport_by_id(id, db)
        stmt = update(models.InlandTransport).values(**values).where(models.InlandTransport.id==id).returning(models.InlandTransport)
        inland_transport = db.execute(stmt).scalars().first()
        if inland_transport is None:
            raise exceptions.ResourceNotFound(resource="Inland transport")
        db.commit()
        return await get_inland_transport_by_id(id, db)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        raise exceptions.classify_foreign_key_violation(error_message, "Inland transport")

async def delete_inland_transport(id: int, db: Session) -> None:
    stmt = delete(models.InlandTransport).where(models.InlandTransport.id==id).returning(models.InlandTransport)
    inland_transport = db.execute(stmt).scalars().first()
    if inland_transport is None:
        raise exceptions.ResourceNotFound(resource="Inland transport") 
    db.commit()

async def get_inland_transport_by_id(id: int, db: Session) -> schemas.InlandTransport:
    stmt = inland_transport_view.filter(models.InlandTransport.id==id)
    inland_transport = db.execute(stmt).mappings().first()
    if inland_transport is None:
        raise exceptions.ResourceNotFound(resource="Inland transport") 
    return schemas.InlandTransport.model_validate(inland_transport)

async def get_inland_transports(db: Session, source_state: str, source_city: str, source_address: str, source_zipcode: str, warehouse_state: str, warehouse_zipcode: str, page: int, limit: int) -> schemas.Pagination[schemas.InlandTransport]:
    where_clause = and_(
        or_(source_state is None, func.lower(models.Source.state)==func.lower(source_state)),
        or_(source_city is None, func.lower(models.Source.city)==func.lower(source_city)),
        or_(source_address is None, func.lower(models.Source.address)==func.lower(source_address)),
        or_(source_zipcode is None, func.lower(models.Source.zipcode)==func.lower(source_zipcode)),
        or_(warehouse_state is None, func.lower(models.Warehouse.state)==func.lower(warehouse_state)),
        or_(warehouse_zipcode is None, func.lower(models.Warehouse.zipcode)==func.lower(warehouse_zipcode))
    )  
    stmt = inland_transport_view.where(where_clause).order_by(models.Source.state, models.Source.city, models.Warehouse.state, models.Warehouse.city, models.InlandTransport.id).offset((page-1)*limit).limit(limit)
    data = [schemas.InlandTransport.model_validate(inland_transport) for inland_transport in db.execute(stmt).mappings().all()]
    total_rows = db.execute(select(func.count()).select_from(inland_transport_view.where(where_clause))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.InlandTransport](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response

async def get_cost_between(source_id: int, warehouse_id: int, db: Session) -> float:
    cost = db.execute(
        select(models.InlandTransport.cost).where(and_(
            models.InlandTransport.source_id==source_id,
            models.InlandTransport.warehouse_id==warehouse_id,
            )
        )
    ).scalar()
    if cost is None:
        raise exceptions.ResourceNotFound(resource="Inland Transport")
    return cost
