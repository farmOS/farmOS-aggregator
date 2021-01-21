import logging

from app.db.session import SessionLocal


# A special FastAPI dependency used to get a SQLAlchemy session
# and ensure it is closed after sending an HTTP response.
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_db():
    db = SessionLocal()
    try:
        logging.debug('Creating DB Session.')
        yield db
    finally:
        logging.debug('Closing DB Session.')
        db.close()
