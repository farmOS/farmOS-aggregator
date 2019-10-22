from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base


class Farm(Base):
    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    farm_name = Column(String, index=True)
    url = Column(String, index=True, unique=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
