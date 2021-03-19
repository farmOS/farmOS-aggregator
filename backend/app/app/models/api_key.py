from sqlalchemy import Column, Boolean, Integer, String, DateTime, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.base_class import Base


class ApiKey(Base):
    __tablename__ = "apikey"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    key = Column(LargeBinary)
    enabled = Column(Boolean, default=False)
    name = Column(String)
    notes = Column(String)
    farm_id = Column(ARRAY(Integer))
    all_farms = Column(Boolean, default=False)
    scopes = Column(ARRAY(String))
