from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AdditionalSettings(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_fee: float
    additional_copart_fee: float
    additional_iaai_fee: float

class AdditionalSettingsUpdate(BaseModel):
    company_fee: Optional[float] = None
    additional_copart_fee: Optional[float] = None
    additional_iaai_fee: Optional[float] = None
