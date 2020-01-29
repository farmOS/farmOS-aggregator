from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class FarmToken(Base):
    __tablename__ = 'farmtoken'

    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    expires_in = Column(String)
    refresh_token = Column(String)
    expires_at = Column(String)

    farm_id = Column(Integer, ForeignKey("farm.id"), unique=True)
    farm = relationship("Farm", uselist=False, back_populates="token")
