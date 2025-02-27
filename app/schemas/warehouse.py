from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from typing import Optional, Annotated

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)] 

class Warehouse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    state: NonEmptyStr
    city: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]

class WarehouseCreate(BaseModel):
    state: NonEmptyStr
    city: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]

    @field_validator('state', mode='before')
    def capitalize_string(cls, v):
        if v:
            return v.strip().upper()
        return v
    
    @field_validator('city', 'address', 'zipcode', mode='before')
    def capitalize_first_letter(cls, v):
        if v:
            return v.strip().title()
        return v

class WarehouseUpdate(BaseModel):
    state: Optional[NonEmptyStr] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None

    @field_validator('state', mode='before')
    def capitalize_string(cls, v):
        if v:
            return v.strip().upper()
        return v
    
    @field_validator('city', 'address', 'zipcode', mode='before')
    def capitalize_first_letter(cls, v):
        if v:
            return v.strip().title()
        return v

