from ..core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    state = Column("state", String)
    zipcode = Column("zipcode", String)
    city = Column("city", String, nullable=True)
    address = Column("address", String, nullable=True)
    __table_args__ = (UniqueConstraint('zipcode', name="unique_zipcode_non_null"),)

