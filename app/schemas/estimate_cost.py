from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .. import models

class CarInfo(BaseModel):
    manufacturer: str
    country: str
    year: int

class EstimateCostRequest(BaseModel):
    amount: float
    auction: models.Auction
    source: int
    warehouse: int
    shipping_line: int
    shipping_type: int
    vin: str

class EstimateCostResponse(CarInfo):
    cost: float

