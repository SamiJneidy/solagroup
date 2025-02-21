from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AdditionalSettings(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    additional_fee: float

class AdditionalSettingsUpdate(BaseModel):
    additional_fee: Optional[float] = None
