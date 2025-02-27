from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends
from typing import Optional
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def update_additional_settings(data: schemas.AdditionalSettingsUpdate, db: Session) -> schemas.AdditionalSettings:
    values: dict = data.model_dump(exclude_unset=True)
    if values == {}:
        return await get_additional_settings(db)
    stmt = update(models.AdditionalSettings).values(**values).returning(models.AdditionalSettings)
    additional_settings = db.execute(stmt).scalars().first()
    db.commit()
    return additional_settings

async def get_additional_settings(db: Session) -> schemas.AdditionalSettings:
    stmt = select(models.AdditionalSettings)
    additional_settings = schemas.AdditionalSettings.model_validate(db.execute(stmt).scalars().first())
    return additional_settings

async def get_additional_fee(db: Session) -> float:
    stmt = select(models.AdditionalSettings.additional_fee)
    additional_fee = db.execute(stmt).scalar()
    return additional_fee
