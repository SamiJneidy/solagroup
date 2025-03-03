from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from typing import Optional
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def update_auction_fee(id: int, data: schemas.AuctionFeeUpdate, db: Session) -> schemas.AuctionFee:
    values: dict = data.model_dump(exclude_unset=True)
    if values == {}:
        return await get_auction_fee_by_id(id, db)
    stmt = update(models.AuctionFee).values(**values).where(models.AuctionFee.id==id).returning(models.AuctionFee)
    auction_fee = db.execute(stmt).scalars().first()
    if auction_fee is None:
        raise exceptions.ResourceNotFound(resource="Auction fee")
    db.commit()
    return schemas.AuctionFee.model_validate(auction_fee)

async def get_auction_fee_by_id(id: int, db: Session) -> schemas.AuctionFee:
    stmt = select(models.AuctionFee).filter(models.AuctionFee.id==id)
    auction_fee = db.execute(stmt).scalars().first()
    if auction_fee is None:
        raise exceptions.ResourceNotFound(resource="Auction fee")
    return schemas.AuctionFee.model_validate(auction_fee)

async def get_auction_fees(db: Session, page: int = 1, limit: int = 10, auction: Optional[schemas.Auction] = None) -> schemas.Pagination[schemas.AuctionFee]:
    stmt = select(models.AuctionFee).where(or_(auction==None, models.AuctionFee.auction==auction)).order_by(models.AuctionFee.id).offset((page-1)*limit).limit(limit)
    data = [schemas.AuctionFee.model_validate(auction_fee) for auction_fee in db.execute(stmt).scalars().all()]
    total_rows = db.execute(select(func.count(models.AuctionFee.id)).where(or_(auction==None, models.AuctionFee.auction==auction))).scalar()
    total_pages = (total_rows + limit - 1) // limit
    response = schemas.Pagination[schemas.AuctionFee](data=data, total_rows=total_rows, total_pages=total_pages, current_page=page, limit=limit)
    return response

async def get_auction_fee(amount: float, auction: schemas.Auction, db: Session) -> float:
    stmt = select(models.AuctionFee).where(and_(models.AuctionFee.auction==auction, models.AuctionFee.range_from <= amount, models.AuctionFee.range_to >= amount))
    auctioin_fee = db.execute(stmt).scalars().first()
    if auctioin_fee.range_to >= 0:
        return auctioin_fee.fee
    return amount*auctioin_fee.fee/100
