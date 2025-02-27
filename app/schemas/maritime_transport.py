from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MaritimeTransport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    warehouse_id: int
    warehouse_state: str
    warehouse_zipcode: str
    shipping_line_id: int
    shipping_line_name: str
    destination_id: int
    destination_country: str
    destination_port: str
    cost: float

class MaritimeTransportCreate(BaseModel):
    warehouse_id: int
    shipping_line_id: int
    destination_id: int
    cost: float

class MaritimeTransportUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    shipping_line_id: Optional[int] = None
    destination_id: Optional[int] = None
    cost: Optional[float] = None
