from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, deferred
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.models.farm_token import FarmToken


class Farm(Base):
    __tablename__ = "farm"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True))
    farm_name = Column(String, index=True)
    url = Column(String, index=True, unique=True)
    notes = Column(String, nullable=True)
    tags = Column(String, nullable=True)

    # Save a space separated list of OAuth Scopes
    scope = Column(String, nullable=True)

    # active attribute allows admins to disable farmOS profiles
    active = Column(Boolean, default=False)

    # Store farm info in a JSONB column
    info = deferred(Column(JSONB, nullable=True))

    is_authorized = Column(Boolean, default=False)
    token = relationship(
        "FarmToken", uselist=False, back_populates="farm", lazy="joined"
    )
    auth_error = Column(String, nullable=True)
