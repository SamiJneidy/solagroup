from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AdditionalSettings(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_fee: float
    additional_auction_fee: float

class AdditionalSettingsUpdate(BaseModel):
    company_fee: Optional[float] = None
    additional_auction_fee: Optional[float] = None
