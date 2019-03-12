""" This file (test_auth.py) tests the basic authentication of the client

"""
import base64
from farmOSaggregator import farmOSaggregator

def login(client_secure, username, password):
    encoded_credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')
    headers = {'Authorization': 'Basic ' + encoded_credentials }
    #return client.get("/", headers=headers)
    return client_secure.get("/", headers=headers)

def test_valid_login(client_secure):
    """
    GIVEN a Flask app
    WHEN the '/' page is requested with valid credentials
    THEN check the page is loaded
    """
    response = login(client_secure, farmOSaggregator.app.config['BASIC_AUTH_USERNAME'], farmOSaggregator.app.config['BASIC_AUTH_PASSWORD'])

    assert response.status_code == 200
    assert b'There are no items in the table.' in response.data
