from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoginCredentials(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str
    token: str

class TokenPayload(BaseModel):
    iat: Optional[datetime] = None
    exp: Optional[datetime] = None
    username: str