from ..core.database import Base
from enum import Enum
from sqlalchemy import Column, Integer, Float, String, DateTime, Enum as SQLEnum

class Auction(Enum):
    COPART = 1
    IAAI = 2

class AuctionFee(Base):
    __tablename__ = "auction_fees"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    range_from = Column("range_from", Float, nullable=False)
    range_to = Column("range_to", Float, nullable=False)
    auction = Column("auction", SQLEnum(Auction), nullable=False)
    fee = Column("fee", Float, nullable=False)

