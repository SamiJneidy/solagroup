from ..core.database import Base
from enum import Enum
from sqlalchemy import Column, Integer, Float, String, DateTime, Enum as SQLEnum

class AdditionalSettings(Base):
    __tablename__ = "additional_settings"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    company_fee = Column("company_fee", Float, nullable=False)
    additional_auction_fee = Column("additional_auction_fee", Float, nullable=False)

