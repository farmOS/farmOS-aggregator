from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo_pool=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
