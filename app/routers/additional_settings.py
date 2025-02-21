from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, models
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/additional-settings")

@router.get(path="/get", response_model=schemas.AdditionalSettings, status_code=status.HTTP_200_OK, tags=["Additional settings"])
async def get_additional_settings(db: Session = Depends(get_db)):
    return await crud.additional_settings.get_additional_settings(db)

@router.put(path="/update", response_model=schemas.AdditionalSettingsUpdate, status_code=status.HTTP_200_OK, tags=["Additional settings"])
async def update_additional_settings(data: schemas.AdditionalSettingsUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.additional_settings.update_additional_settings(data, db)
