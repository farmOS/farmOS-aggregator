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

    # Disable HTTP Basic Auth by default
    farmOSaggregator.app.config['BASIC_AUTH_FORCE'] = False

    client = farmOSaggregator.app.test_client()

    ctx = farmOSaggregator.app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def client_secure():
    farmOSaggregator.app.config['TESTING'] = True

    # Enable HTTP Basic Auth by default
    farmOSaggregator.app.config['BASIC_AUTH_FORCE'] = True

    client = farmOSaggregator.app.test_client()

    ctx = farmOSaggregator.app.app_context()
    ctx.push()

    yield client

    ctx.pop()
