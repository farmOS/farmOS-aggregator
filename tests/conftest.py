"""
pytest configuration file.

Includes fixtures for unit and functional tests
"""
 
import pytest
from farmOSaggregator.models import Farm
 
@pytest.fixture(scope='module')
def new_farm():
    farm = Farm('test.url', 'test name', 'testusername', 'testpass')
    return farm
