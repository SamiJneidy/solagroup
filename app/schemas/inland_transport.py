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
    destination_id: int
    destination_state: str
    destination_zipcode: str
    cost: float

class InlandTransportCreate(BaseModel):
    source_id: int
    destination_id: int
    cost: float

class InlandTransportUpdate(BaseModel):
    source_id: Optional[int] = None
    destination_id: Optional[int] = None
    cost: Optional[float] = None
