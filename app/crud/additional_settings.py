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

async def get_additional_settings(db: Session) -> schemas.Pagination[schemas.AdditionalSettings]:
    stmt = select(models.AdditionalSettings)
    data = [schemas.AdditionalSettings.model_validate(db.execute(stmt).scalars().first())]
    response = schemas.Pagination[schemas.AdditionalSettings](data=data, total_rows=1, total_pages=1, current_page=1, limit=1)
    return response
