from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select
from datetime import datetime, timedelta
from fastapi import Depends
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def get_user_by_username(username: str, db: Session) -> schemas.User:
    user: models.User = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        raise exceptions.UserNotFound()
    return schemas.User.model_validate(user)

async def get_user_by_id(id: int, db: Session) -> schemas.User:
    user: models.User = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise exceptions.UserNotFound()
    return schemas.User.model_validate(user)

async def get_users(db: Session) -> list[schemas.UserGet]:
    users = [schemas.UserGet.model_validate(user) for user in db.execute(select(models.User)).scalars().all()]
    return users