from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Warehouse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    state: str
    city: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]

class WarehouseCreate(BaseModel):
    state: str
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None

class WarehouseUpdate(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None
