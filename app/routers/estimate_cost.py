from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, models
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/estimate-cost")

@router.post(path="", response_model=schemas.EstimateCostResponse, status_code=status.HTTP_200_OK, tags=["Estimate cost"])
async def estimate_cost(data: schemas.EstimateCostRequest, db: Session = Depends(get_db)):
    return await crud.estimate_cost.estimate_cost(data, db)
