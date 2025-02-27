from pydantic import BaseModel, ConfigDict, field_validator, StringConstraints
from typing import Optional, Annotated

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]

class ShippingLine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: NonEmptyStr

class ShippingLineCreate(BaseModel):
    name: NonEmptyStr

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if v is None:
            raise ValueError("name must not be null")
        return v.strip().upper()

class ShippingLineUpdate(BaseModel):
    name: Optional[NonEmptyStr] = None

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if v is None:
            raise ValueError("name cannot be null")
        return v.strip().upper()
