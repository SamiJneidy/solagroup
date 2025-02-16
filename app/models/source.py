from ..core.database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime

class Source(Base):
    __tablename__ = "sources"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    state = Column("state", String)
    city = Column("city", String)
    address = Column("address", String)
    zipcode = Column("zipcode", String, unique=True)
