from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, func
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def get_user_by_username(username: str, db: Session) -> schemas.User:
    user: models.User = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        raise exceptions.ResourceNotFound("Username")
    return schemas.User.model_validate(user)

async def get_user_by_id(id: int, db: Session) -> schemas.User:
    user: models.User = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise exceptions.ResourceNotFound("Username")
    return schemas.User.model_validate(user)

async def get_users(db: Session, page: int = 1, limit: int = 10) -> schemas.Pagination[schemas.UserGet]:
    stmt = select(models.User).order_by(models.User.id).offset((page-1)*limit).limit(limit)
    data = [schemas.UserGet.model_validate(user) for user in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.User.id))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.UserGet](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response