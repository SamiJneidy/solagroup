from ..core.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    username = Column("username", String, nullable=False, unique=True, index=True)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(tz=timezone.utc))