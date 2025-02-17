from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class InlandTransport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    source_state: str
    source_city: str
    source_address: str
    source_zipcode: str
    warehouse_id: int
    warehouse_state: str
    warehouse_zipcode: str
    cost: float

class InlandTransportCreate(BaseModel):
    source_id: int
    warehouse_id: int
    cost: float

class InlandTransportUpdate(BaseModel):
    source_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    cost: Optional[float] = None
