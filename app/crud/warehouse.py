from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, distinct, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def create_warehouse(data: schemas.WarehouseCreate, db: Session) -> schemas.Warehouse:
    try:
        stmt = insert(models.Warehouse).values(**data.model_dump()).returning(models.Warehouse)
        inserted_warehouse = db.execute(stmt).scalars().first()
        db.commit()
        return schemas.Warehouse.model_validate(inserted_warehouse)
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse(resource="Zipcode")

async def update_warehouse(id: int, data: schemas.WarehouseUpdate, db: Session) -> schemas.Warehouse:
    try:
        values: dict = data.model_dump(exclude_unset=True)
        if values == {}:
            return await get_warehouse_by_id(id, db)
        stmt = update(models.Warehouse).values(**values).where(models.Warehouse.id==id).returning(models.Warehouse)
        warehouse = db.execute(stmt).scalars().first()
        if warehouse is None:
            raise exceptions.ResourceNotFound(resource="Warehouse")
        db.commit()
        return schemas.Warehouse.model_validate(warehouse)   
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse(resource="Zipcode")

async def delete_warehouse(id: int, db: Session) -> None:
    try:
        stmt = delete(models.Warehouse).where(models.Warehouse.id==id).returning(models.Warehouse)
        warehouse = db.execute(stmt).scalars().first()
        if warehouse is None:
            raise exceptions.ResourceNotFound(resource="Warehouse")
        db.commit()
    except IntegrityError:
        raise exceptions.ForeignKeyConstraintViolation()
    
async def get_warehouse_by_id(id: int, db: Session) -> schemas.Warehouse:
    stmt = select(models.Warehouse).filter(models.Warehouse.id==id)
    warehouse = db.execute(stmt).scalars().first()
    if warehouse is None:
        raise exceptions.ResourceNotFound(resource="Warehouse")
    return schemas.Warehouse.model_validate(warehouse)

async def get_warehouse_by_zipcode(zipcode: str, db: Session) -> schemas.Warehouse:
    stmt = select(models.Warehouse).filter(models.Warehouse.zipcode==zipcode)
    warehouse = db.execute(stmt).scalars().first()
    if warehouse is None:
        raise exceptions.ResourceNotFound(resource="Warehouse")
    return schemas.Warehouse.model_validate(warehouse)

async def get_warehouses(db: Session, page: int, limit: int) -> schemas.Pagination[schemas.Warehouse]:
    stmt = select(models.Warehouse).order_by(models.Warehouse.state, models.Warehouse.city, models.Warehouse.zipcode, models.Warehouse.id)
    if page is not None and limit is not None:
        stmt = stmt.offset((page-1)*limit).limit(limit)
    data = [schemas.Warehouse.model_validate(warehouse) for warehouse in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.Warehouse.id))).scalar()
    total_pages = None if limit is None else (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.Warehouse](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response

async def get_warehouses_order_by_cost(db: Session, source_id: int, shipping_line_id: int, destination_country: str, destination_port: str, page: int, limit: int) -> schemas.Pagination[schemas.Warehouse]:
    view = select(
        models.Warehouse.id,
        models.Warehouse.state,
        models.Warehouse.city,
        models.Warehouse.zipcode,
        models.Warehouse.address,
        func.min(models.InlandTransport.cost+models.MaritimeTransport.cost).label("total_cost")
    ).join(models.InlandTransport, models.InlandTransport.warehouse_id==models.Warehouse.id
    ).join(models.MaritimeTransport, models.MaritimeTransport.warehouse_id==models.Warehouse.id
    ).join(models.ShippingLine, models.MaritimeTransport.shipping_line_id==models.ShippingLine.id
    ).join(models.Destination, models.MaritimeTransport.destination_id==models.Destination.id
    ).group_by(
        models.Warehouse.id,
        models.Warehouse.state,
        models.Warehouse.city,
        models.Warehouse.zipcode,
        models.Warehouse.address,
    )
    where_clause = and_(
        or_(source_id is None, models.InlandTransport.source_id==source_id),
        or_(shipping_line_id is None, models.MaritimeTransport.shipping_line_id==shipping_line_id),
        or_(destination_country is None, models.Destination.country==destination_country),
        or_(destination_port is None, models.Destination.port==destination_port),
    )
    stmt = view.where(where_clause).order_by(
        func.min(models.InlandTransport.cost+models.MaritimeTransport.cost)
    )
    if page is not None and limit is not None:
        stmt = stmt.offset((page-1)*limit).limit(limit)
    data = [schemas.Warehouse.model_validate(warehouse) for warehouse in db.execute(stmt).mappings().all()]
    total_rows = db.execute(select(func.count()).select_from(stmt)).scalar()
    total_pages = None if limit is None else (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.Warehouse](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response
