from ..core.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class InlandTransport(Base):
    __tablename__ = "inland_transport"
    id = Column("id", Integer, primary_key=True)
    source_id = Column("source_id", Integer, ForeignKey("sources.id"), nullable=False)
    destination_id = Column("destination_id", Integer, ForeignKey("destinations.id"), nullable=False)
    cost = Column("cost", Float, nullable=False)
    __table_args__ = (UniqueConstraint('source_id', 'destination_id', name="unique_source_destination"),)
