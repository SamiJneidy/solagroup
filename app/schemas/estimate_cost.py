from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .. import models

class CarInfo(BaseModel):
    manufacturer: Optional[str] = None
    country: Optional[str] = None
    year: Optional[int] = None

class EstimateCostRequest(BaseModel):
    amount: float
    auction: models.Auction
    source: int
    warehouse: int
    shipping_line: int
    shipping_type: int
    vin: Optional[str] = None

class EstimateCostResponse(CarInfo):
    cost: float

