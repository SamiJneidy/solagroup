from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func
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
        raise exceptions.ResourceAlreadyInUse("Zipcode")

async def update_warehouse(id: int, data: schemas.WarehouseUpdate, db: Session) -> schemas.Warehouse:
    try:
        values: dict = data.model_dump(exclude_none=True, exclude_unset=True)
        if values == {}:
            return await get_warehouse_by_id(id, db)
        stmt = update(models.Warehouse).values(**values).where(models.Warehouse.id==id).returning(models.Warehouse)
        warehouse = db.execute(stmt).scalars().first()
        if warehouse is None:
            raise exceptions.ResourceNotFound("Warehouse")
        db.commit()
        return schemas.Warehouse.model_validate(warehouse)   
    except IntegrityError:
        raise exceptions.ResourceAlreadyInUse("Zipcode")

async def delete_warehouse(id: int, db: Session) -> None:
    stmt = delete(models.Warehouse).where(models.Warehouse.id==id).returning(models.Warehouse)
    warehouse = db.execute(stmt).scalars().first()
    if warehouse is None:
        raise exceptions.ResourceNotFound("Warehouse")
    db.commit()

async def get_warehouse_by_id(id: int, db: Session) -> schemas.Warehouse:
    stmt = select(models.Warehouse).filter(models.Warehouse.id==id)
    warehouse = db.execute(stmt).scalars().first()
    if warehouse is None:
        raise exceptions.ResourceNotFound("Warehouse")
    return schemas.Warehouse.model_validate(warehouse)

async def get_warehouse_by_zipcode(zipcode: str, db: Session) -> schemas.Warehouse:
    stmt = select(models.Warehouse).filter(models.Warehouse.zipcode==zipcode)
    warehouse = db.execute(stmt).scalars().first()
    if warehouse is None:
        raise exceptions.ResourceNotFound("Warehouse")
    return schemas.Warehouse.model_validate(warehouse)

async def get_warehouses(db: Session, page: int = 1, limit: int = 10) -> schemas.Pagination[schemas.Warehouse]:
    stmt = select(models.Warehouse).offset((page-1)*limit).limit(limit)
    data = [schemas.Warehouse.model_validate(warehouse) for warehouse in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.Warehouse.id))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.Warehouse](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response