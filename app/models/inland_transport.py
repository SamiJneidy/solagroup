from ..core.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class InlandTransport(Base):
    __tablename__ = "inland_transport"
    id = Column("id", Integer, primary_key=True)
    source_id = Column("source_id", Integer, ForeignKey("sources.id"), nullable=False)
    warehouse_id = Column("warehouse_id", Integer, ForeignKey("warehouses.id"), nullable=False)
    cost = Column("cost", Float, nullable=False)
    __table_args__ = (UniqueConstraint('source_id', 'warehouse_id', name="unique_source_warehouse"),)
