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
from farmOSaggregator import create_app, farmOSaggregator
from farmOSaggregator.models import Farm, db

@pytest.fixture(scope='module')
def new_farm():
    farm = Farm('test.url', 'test name', 'testusername', 'testpass')
    return farm

@pytest.fixture(scope='module')
def client():
    app = create_app('tests.cfg')

    # Create temporary database
    db_fd, db_filepath = tempfile.mkstemp()
    farmOSaggregator.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_filepath

    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    # Delete temp datbase
    os.close(db_fd)
    os.unlink(db_filepath)

    ctx.pop()

@pytest.fixture(scope='module')
def client_secure():
    # Create temporary database
    db_fd, db_filepath = tempfile.mkstemp()
    farmOSaggregator.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_filepath
    app = create_app('tests_secure.cfg')

    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    # Delete temp datbase
    os.close(db_fd)
    os.unlink(db_filepath)

    ctx.pop()
