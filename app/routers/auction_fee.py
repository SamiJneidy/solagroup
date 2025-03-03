from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, models
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/auction-fees")


@router.get(
    path="/get/id/{id}",
    response_model=schemas.AuctionFee,
    responses={
        status.HTTP_200_OK: {
            "description": "Auction fee returned successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Auction fee not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Auction fee not found": {
                            "value": {"detail": "Auction fee not found"}
                        }
                    }
                }
            }
        },
    },
    tags=["Auction fees"],
)
async def get_auction_fee_by_id(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return await crud.auction_fee.get_auction_fee_by_id(id, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.AuctionFee],
    responses = {
        status.HTTP_200_OK: {
            "description": "Auction fees returned successfully",
        },
    },
    tags=["Auction fees"],
)
async def get_auction_fees(
    page: int = 1,
    limit: int = 10,
    auction: Optional[schemas.Auction] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await crud.auction_fee.get_auction_fees(db, page, limit, auction)


@router.put(
    path="/update/{id}",
    response_model=schemas.AuctionFee,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Auction fee updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Auction fee not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Auction fee Not Found": {
                            "value": {"detail": "Auction fee not found"}
                        }
                    }
                }
            }
        },
    },
    tags=["Auction fees"],
)
async def update_auction_fee(
    id: int,
    data: schemas.AuctionFeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.auction_fee.update_auction_fee(id, data, db)
