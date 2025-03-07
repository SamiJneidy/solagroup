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
    additional_fees: schemas.Pagination[schemas.AdditionalSettings] = await additional_settings.get_additional_settings(db)
    company_fee = additional_fees.data[0].company_fee
    additional_auction_fee = additional_fees.data[0].additional_auction_fee
    
    # virtual bid fee ranges and values in copart and iaai are the same
    virtual_bid_fees = [ 
        #[from, to, fee]
        [0, 100, 0],
        [100, 500, 50],
        [500, 1000, 65],
        [1000, 1500, 85],
        [1500, 2000, 95],
        [2000, 4000, 110],
        [4000, 6000, 125],
        [6000, 8000, 145],
        [8000, 1000000000, 160]
    ]
    environmental_fee = 15 # the same in copart and iaai
    gate_fee = 95 # service fee in iaai
    title_pickup_fee = 20 # title handling fee in iaai
    virtual_bid_fee = 0 # internet bid fee in iaai

    for i in virtual_bid_fees:
        if data.amount in range(i[0], i[1]):
            virtual_bid_fee = i[2]
            break
    
    auction_fee_amount: float = (
        await auction_fee.get_auction_fee(data.amount, data.auction, db)
        + environmental_fee
        + gate_fee
        + title_pickup_fee
        + virtual_bid_fee
        + additional_auction_fee
    )
    total_cost = (
        data.amount
        + inland_transport_cost
        + auction_fee_amount
        + company_fee
        + maritime_transport_cost / data.shipping_type
    )
    car_info = await utils.decode_vin(data.vin)
    response = schemas.EstimateCostResponse(
        amount=data.amount,
        inland_transport_cost=inland_transport_cost,
        maritime_transport_cost=maritime_transport_cost,
        auction_fee=auction_fee_amount,
        company_fee=company_fee,
        total_cost=total_cost,
        **car_info.model_dump()
    )
    return response
