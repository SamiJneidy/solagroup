from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class Source(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    state: str
    city: str
    address: str
    zipcode: str

class SourceCreate(BaseModel):
    state: str
    city: str
    address: str
    zipcode: str

    @field_validator("state", "city", "address", "zipcode")
    @classmethod
    def not_empty_str(cls, value, field):
        if value.strip() == "":
            raise ValueError(f"{field.name} must not be an empty string")
        return value


class SourceUpdate(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None
    
    @field_validator("state", "city", "address", "zipcode")
    @classmethod
    def not_empty_str(cls, value, field):
        if value is not None and value.strip() == "":
            raise ValueError(f"{field.name} must not be an empty string")
        return value
