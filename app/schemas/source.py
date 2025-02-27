from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from datetime import datetime
from typing import Optional, Annotated

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)] 

class Source(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    state: NonEmptyStr
    city: NonEmptyStr
    address: NonEmptyStr
    zipcode: NonEmptyStr

class SourceCreate(BaseModel):
    state: NonEmptyStr
    city: NonEmptyStr
    address: NonEmptyStr
    zipcode: NonEmptyStr

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

class SourceUpdate(BaseModel):
    state: Optional[NonEmptyStr] = None
    city: Optional[NonEmptyStr] = None
    address: Optional[NonEmptyStr] = None
    zipcode: Optional[NonEmptyStr] = None

    @field_validator('state', mode='before')
    def capitalize_string(cls, v):
        if v is None:
            raise ValueError("field cannot be null")
        return v.strip().upper()
    
    @field_validator('city', 'address', 'zipcode', mode='before')
    def capitalize_first_letter(cls, v):
        if v is None:
            raise ValueError("field cannot be null")
        return v.strip().title()
