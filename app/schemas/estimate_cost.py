from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .. import models, schemas

class CarInfo(BaseModel):
    manufacturer: Optional[str] = None
    country: Optional[str] = None
    year: Optional[int] = None

class EstimateCostRequest(BaseModel):
    amount: float
    auction: schemas.Auction
    source: int
    shipping_line: int
    shipping_type: int
    destination_country: str
    destination_port: str
    warehouse: int
    vin: Optional[str] = None

class EstimateCostResponse(CarInfo):
    amount: float
    inland_transport_cost: float
    maritime_transport_cost: float
    auction_fee: float
    company_fee: float
    total_cost: float

