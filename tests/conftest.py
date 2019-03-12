"""
pytest configuration file.

Includes fixtures for unit and functional tests
"""

import pytest

from farmOSaggregator import farmOSaggregator, db
from farmOSaggregator.models import Farm

@pytest.fixture(scope='module')
def new_farm():
    farm = Farm('test.url', 'test name', 'testusername', 'testpass')
    return farm

@pytest.fixture(scope='module')
def client():
    farmOSaggregator.app.config['TESTING'] = True
    client = farmOSaggregator.app.test_client()

    ctx = farmOSaggregator.app.app_context()
    ctx.push()

    yield client

    ctx.pop()
