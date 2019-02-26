# Import SQLAlchemy packages
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Initialize a declarative base class.
Base = declarative_base()


class Farm(Base):
    """Define the farm database model."""
    __tablename__ = 'farm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(), index=True, nullable=False)
    farm_name = Column(String(), index=True, nullable=False)
    username = Column(String(), index=True)
    password = Column(String())

    def __str__(self):
        return "{}".format(self.url)

    def __repr__(self):
        return '<Farm {}>'.format(self.__str__())
