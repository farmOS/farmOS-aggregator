"""
Unit tests for the models.py file
"""

def test_new_farm(new_farm):
    """
    GIVEN a Farm model
    WHEN a new Farm is created
    THEN check the URL, farm name, username and password are defined correctly
    """
    assert new_farm.url == 'test.url'
    assert new_farm.farm_name == 'test name'
    assert new_farm.username == 'testusername'
    assert new_farm.password == 'testpass'
