"""
pytest configuration file.

Includes fixtures for unit and functional tests
"""
import os
import tempfile

import pytest
from flask_sqlalchemy import SQLAlchemy

from farmOSaggregator import farmOSaggregator
from farmOSaggregator.models import Farm

@pytest.fixture(scope='module')
def new_farm():
    farm = Farm('test.url', 'test name', 'testusername', 'testpass')
    return farm

@pytest.fixture(scope='module')
def client():
    farmOSaggregator.app.config['TESTING'] = True

    # Disable HTTP Basic Auth by default
    farmOSaggregator.app.config['BASIC_AUTH_FORCE'] = False

    # Create temporary database
    db_fd, db_filepath = tempfile.mkstemp()
    farmOSaggregator.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_filepath

    client = farmOSaggregator.app.test_client()

    ctx = farmOSaggregator.app.app_context()
    ctx.push()

    # Initialize DB
    db = SQLAlchemy(farmOSaggregator.app)
    farmOSaggregator.models.Base.metadata.create_all(db.engine)

    yield client

    # Delete temp datbase
    os.close(db_fd)
    os.unlink(db_filepath)

    ctx.pop()

@pytest.fixture(scope='module')
def client_secure():
    farmOSaggregator.app.config['TESTING'] = True

    # Enable HTTP Basic Auth by default
    farmOSaggregator.app.config['BASIC_AUTH_FORCE'] = True

    # Create temporary database
    db_fd, db_filepath = tempfile.mkstemp()
    farmOSaggregator.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_filepath

    client = farmOSaggregator.app.test_client()

    ctx = farmOSaggregator.app.app_context()
    ctx.push()

    # Initialize DB
    db = SQLAlchemy(farmOSaggregator.app)
    farmOSaggregator.models.Base.metadata.create_all(db.engine)

    yield client

    # Delete temp datbase
    os.close(db_fd)
    os.unlink(db_filepath)

    ctx.pop()
