import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

def test_create_term(test_farm, test_term):
    server_api = get_server_api()

    data = test_term

    response = requests.post(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}",
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check term was created
    test_farm_terms = content[str(test_farm.id)]
    assert len(test_farm_terms) == 1
    assert 'id' in test_farm_terms[0]
    created_term_id = test_farm_terms[0]['id']
    test_term['id'] = created_term_id

    # Check that the creats term has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}&tid={test_term['id']}",
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    created_term = content[str(test_farm.id)][0]
    # Check attributes
    assert created_term['name'] == data['name']
    # Check that an optional attribute was populated
    assert data['description'] in created_term['description']

def test_get_terms(test_farm):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}",
    )
    # Check response
    assert 200 <= r.status_code < 300
    terms = r.json()

    # Check farm ID included in response
    assert str(test_farm.id) in terms

    # Check terms are returned for the farm
    test_farm_terms = terms[str(test_farm.id)]
    assert len(test_farm_terms) > 1
    for term in test_farm_terms:
        assert "name" in term

    assert str(test_farm.id) in terms

    test_farm_terms = terms[str(test_farm.id)]
    assert len(test_farm_terms) > 1
    for term in test_farm_terms:
        assert "name" in term

def test_update_term(test_farm, test_term):
    server_api = get_server_api()

    # Change term attributes
    test_term['name'] = "Updated name from farmOS-aggregator"
    test_term['description'] = "Updated description from farmOS-aggregator"
    data = test_term

    response = requests.put(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}",
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check that the updated term has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}&tid={test_term['id']}",
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    updated_term = content[str(test_farm.id)][0]
    # Check attributes
    assert updated_term['name'] == data['name']
    # Check that an optional attribute was updated
    assert data['description'] in updated_term['description']

