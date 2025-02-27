from ..core.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class MaritimeTransport(Base):
    __tablename__ = "maritime_transport"
    id = Column("id", Integer, primary_key=True)
    warehouse_id = Column("warehouse_id", Integer, ForeignKey("warehouses.id"), nullable=False)
    shipping_line_id = Column("shipping_line_id", Integer, ForeignKey("shipping_lines.id"), nullable=False)
    destination_id = Column("destination_id", Integer, ForeignKey("destinations.id"), nullable=False)
    cost = Column("cost", Float, nullable=False)
    __table_args__ = (
        UniqueConstraint('warehouse_id', 'shipping_line_id', 'destination_id', name="unique_warehouse_shipping_line_destination"),
    )
