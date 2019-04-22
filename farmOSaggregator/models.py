# Import SQLAlchemy.
from flask_sqlalchemy import SQLAlchemy

# Create db extension object in models file per
#   http://flask.pocoo.org/docs/1.0/patterns/appfactories/#factories-extensions
db = SQLAlchemy()

# Subclass from db instance, not sqlalcemy.model per
#   http://flask-sqlalchemy.pocoo.org/2.3/api/#models

class Farm(db.Model):
    """Define the farm database model."""
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(), index=True, nullable=False)
    farm_name = db.Column(db.String(), index=True, nullable=False)
    username = db.Column(db.String(), index=True)
    password = db.Column(db.String())

    def __init__(self, url=None, farm_name=None, username=None, password=None):
        self.url = url
        self.farm_name = farm_name
        self.username = username
        self.password = password

    def __str__(self):
        return "{}".format(self.url)

    def __repr__(self):
        return '<Farm {}>'.format(self.__str__())
