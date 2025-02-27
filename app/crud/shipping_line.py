from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def create_shipping_line(data: schemas.ShippingLineCreate, db: Session) -> schemas.ShippingLine:
    stmt = insert(models.ShippingLine).values(**data.model_dump()).returning(models.ShippingLine)
    inserted_shipping_line = db.execute(stmt).scalars().first()
    db.commit()
    return schemas.ShippingLine.model_validate(inserted_shipping_line)

async def update_shipping_line(id: int, data: schemas.ShippingLineUpdate, db: Session) -> schemas.ShippingLine:
    values: dict = data.model_dump(exclude_unset=True)
    if values == {}:
        return await get_shipping_line_by_id(id, db)
    stmt = update(models.ShippingLine).values(**values).where(models.ShippingLine.id==id).returning(models.ShippingLine)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Shipping line")
    db.commit()
    return schemas.ShippingLine.model_validate(source)

async def delete_shipping_line(id: int, db: Session) -> None:
    stmt = delete(models.ShippingLine).where(models.ShippingLine.id==id).returning(models.ShippingLine)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Shipping line") 
    db.commit()

async def get_shipping_line_by_id(id: int, db: Session) -> schemas.ShippingLine:
    stmt = select(models.ShippingLine).filter(models.ShippingLine.id==id)
    source = db.execute(stmt).scalars().first()
    if source is None:
        raise exceptions.ResourceNotFound("Shipping line") 
    return schemas.ShippingLine.model_validate(source)

async def get_shipping_lines(db: Session, page: int = 1, limit: int = 10) -> schemas.Pagination[schemas.ShippingLine]:
    stmt = select(models.ShippingLine).order_by(models.ShippingLine.name, models.ShippingLine.id).offset((page-1)*limit).limit(limit)
    data = [schemas.ShippingLine.model_validate(shipping_line) for shipping_line in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.ShippingLine.id))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.ShippingLine](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response
