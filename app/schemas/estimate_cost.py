from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .. import models

class EstimateCostRequest(BaseModel):
    amount: float
    auction: models.Auction
    source: int
    warehouse: int
    shipping_line: int
    shipping_type: int
    vin: str

class EstimateCostResponse(BaseModel):
    manufacturer: str
    country: str
    year: int
    cost: float

