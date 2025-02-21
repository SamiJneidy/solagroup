from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .. import models

class AuctionFee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    range_from: float
    range_to: float
    auction: int
    fee: float

class AuctionFeeUpdate(BaseModel):
    fee: float
