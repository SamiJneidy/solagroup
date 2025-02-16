from pydantic import BaseModel, ConfigDict
from datetime import datetime

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    created_at: datetime