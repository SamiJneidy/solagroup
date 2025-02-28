from ..core.database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime

class ShippingLine(Base):
    __tablename__ = "shipping_lines"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    name = Column("name", String, nullable=False, index=True)
