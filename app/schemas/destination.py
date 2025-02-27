from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from datetime import datetime
from typing import Optional, Annotated

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)] 

class Destination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    country: NonEmptyStr
    port: NonEmptyStr

class DestinationCreate(BaseModel):
    country: NonEmptyStr
    port: NonEmptyStr
    
    @field_validator('country', 'port', mode='before')
    def capitalize_string(cls, v):
        if v is None:
            raise ValueError("field cannot be null")
        return v.strip().title()

class DestinationUpdate(BaseModel):
    country: Optional[NonEmptyStr] = None
    port: Optional[NonEmptyStr] = None
    
    @field_validator('country', 'port', mode='before')
    def capitalize_string(cls, v):
        if v is None:
            raise ValueError("field cannot be null")
        return v.strip().title()
