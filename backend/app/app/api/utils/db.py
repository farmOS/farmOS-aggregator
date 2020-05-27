from app.db.session import SessionLocal


# A special FastAPI dependency used to get a SQLAlchemy session
# and ensure it is closed after sending an HTTP response.
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
