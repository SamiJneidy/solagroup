from pydantic import BaseModel, ConfigDict
from typing import Optional

class ShippingLine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class ShippingLineCreate(BaseModel):
    name: str

class ShippingLineUpdate(BaseModel):
    name: Optional[str] = None
