""" This file (test_auth.py) tests the basic authentication of the client

"""
import base64
from farmOSaggregator import farmOSaggregator

def login(client_secure, username, password):
    encoded_credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')
    headers = {'Authorization': 'Basic ' + encoded_credentials }
    #return client.get("/", headers=headers)
    return client_secure.get("/", headers=headers)

def test_login_not_required_for_basic_testing(client):
    """
    GIVEN a Flask app
    WHEN the '/' page is requested without credentials
    THEN check the page is loaded
    """
    response = client.get("/")

    assert response.status_code == 200
    assert b'There are no items in the table.' in response.data

def test_valid_login(client_secure):
    """
    GIVEN a Flask app
    WHEN the '/' page is requested with valid credentials
    THEN check the page is loaded
    """
    response = login(client_secure, farmOSaggregator.default_settings.BASIC_AUTH_USERNAME, farmOSaggregator.default_settings.BASIC_AUTH_PASSWORD)

    assert response.status_code == 200
    assert b'There are no items in the table.' in response.data

def test_invalid_login(client_secure):
    """
    GIVEN a Flask app
    WHEN the '/' page is requested with INVALID credentials
    THEN check the page is NOT loaded
    """
    response = login(client_secure, 'username', 'password')

    assert response.status_code == 401
