from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
from .. import models

class Auction(str, Enum):
    COPART = "COPART"
    IAAI = "IAAI"

class AuctionFee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    range_from: float
    range_to: float
    auction: models.DBAuction
    fee: float

class AuctionFeeUpdate(BaseModel):
    fee: float
