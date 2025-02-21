from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from typing import Optional
from . import inland_transport, maritime_transport, auction_fee, additional_settings
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

async def estimate_cost(data: schemas.EstimateCostRequest, db: Session) -> dict:
    print("Processing inland transport")
    inland_transport_cost: float = await inland_transport.get_inland_transport_between(data.source, data.warehouse, db)
    print("Processing maritime transport")
    maritime_transport_cost: float = await maritime_transport.get_maritime_transport_between(data.warehouse, data.shipping_line, db)
    print("Processing auction fee")
    auction_fee_amount: float = await auction_fee.get_auction_fee(data.amount, data.auction, db)
    print("Processing addtitional fee")
    additional_fee: float = await additional_settings.get_additional_fee(db)
    total_fee = data.amount + inland_transport_cost + auction_fee_amount + additional_fee + maritime_transport_cost/data.shipping_type
    return {"fee": total_fee}
