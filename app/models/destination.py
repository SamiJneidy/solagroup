from ..core.database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime

class Destination(Base):
    __tablename__ = "destinations"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    country = Column("country", String, nullable=False)
    port = Column("port", String, nullable=False)

    __table_args__ = (
        UniqueConstraint('country', 'port', name="unique_country_port"),
    )
