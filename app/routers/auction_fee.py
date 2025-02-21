from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, models
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/auction-fees")

@router.get(path="/get/id/{id}", response_model=schemas.AuctionFee, status_code=status.HTTP_200_OK, tags=["Auction fees"])
async def get_auction_fee_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.auction_fee.get_auction_fee_by_id(id, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.AuctionFee], status_code=status.HTTP_200_OK, tags=["Auction fees"])
async def get_auction_fees(page: int = 1, limit: int = 10, auction: str = Query(None, description="Enter 'COPART' or 'IAAI'"), db: Session = Depends(get_db)):
    return await crud.auction_fee.get_auction_fees(db, page, limit, auction)

@router.put(path="/update/{id}", response_model=schemas.AuctionFee, status_code=status.HTTP_200_OK, tags=["Auction fees"])
async def update_auction_fee(id: int, data: schemas.AuctionFeeUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.auction_fee.update_auction_fee(id, data, db)
