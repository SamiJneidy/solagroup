from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete, func, and_, or_
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from typing import Optional
from . import inland_transport, maritime_transport, auction_fee, additional_settings
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models, utils


async def estimate_cost(
    data: schemas.EstimateCostRequest, db: Session
) -> schemas.EstimateCostResponse:
    inland_transport_cost: float = await inland_transport.get_cost_between(
        data.source, data.warehouse, db
    )
    maritime_transport_cost: float = (
        await maritime_transport.get_maritime_transport_between(
            data.warehouse, data.shipping_line, data.destination_country, data.destination_port, db
        )
    )
    auction_fee_amount: float = await auction_fee.get_auction_fee(
        data.amount, data.auction, db
    )
    additional_fee: float = await additional_settings.get_additional_fee(db)
    total_cost = (
        data.amount
        + inland_transport_cost
        + auction_fee_amount
        + additional_fee
        + maritime_transport_cost / data.shipping_type
    )
    car_info = await utils.decode_vin(data.vin)
    response = schemas.EstimateCostResponse(
        inland_transport_cost=inland_transport_cost,
        maritime_transport_cost=maritime_transport_cost,
        auction_fee=auction_fee_amount,
        total_cost=total_cost,
        **car_info.model_dump()
    )
    return response
