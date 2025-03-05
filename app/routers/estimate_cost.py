from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, models
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(
    prefix="/estimate-cost",
    tags=["Estimate Cost"],
)


@router.post(
    path="",
    response_model=schemas.EstimateCostResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully calculated the cost",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "There is not enough information in the database to calculate the cost based on the specified filters. This may happen due to missing inland or maritime transport data between some of the filters.",
            "content": {
                "application/json": {
                    "examples": {
                        "Inland transport Not Found": {
                            "value": {"detail": "Inland transport not found"}
                        },
                        "Maritime transport Not Found": {
                            "value": {"detail": "Maritime transport not found"}
                        }
                    }
                }
            },
        },
    },
)
async def estimate_cost(
    data: schemas.EstimateCostRequest, db: Session = Depends(get_db)
):
    """Calculates the estimated cost of the vehicle based on the sent filters."""
    return await crud.estimate_cost.estimate_cost(data, db)
