from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Destination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    state: str
    city: str
    address: str
    zipcode: str

class DestinationCreate(BaseModel):
    state: str
    city: str
    address: str
    zipcode: str

class DestinationUpdate(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None
