import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import farmOS_testing_server, get_scope_token_headers


@pytest.fixture
def farm_terms_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:read farm.terms")


@farmOS_testing_server
def test_create_term(client: TestClient, test_farm, test_term, farm_terms_headers):
    data = test_term

    response = client.post(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}",
        headers=farm_terms_headers,
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
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}&tid={test_term['id']}",
        headers=farm_terms_headers,
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


@farmOS_testing_server
def test_get_terms(client: TestClient, test_farm, farm_terms_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}",
        headers=farm_terms_headers,
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


@farmOS_testing_server
def test_update_term(client: TestClient, test_farm, test_term, farm_terms_headers):
    # Change term attributes
    test_term['name'] = "Updated name from farmOS-aggregator"
    test_term['description'] = "Updated description from farmOS-aggregator"
    data = test_term

    response = client.put(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}",
        headers=farm_terms_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    response_term = content[str(test_farm.id)][0]
    assert 'id' in response_term
    assert test_term['id'] == str(response_term['id'])

    # Check that the updated term has correct attributes
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}&tid={test_term['id']}",
        headers=farm_terms_headers,
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


@farmOS_testing_server
def test_delete_term(client: TestClient, test_farm, test_term, farm_terms_headers):
    response = client.delete(
        f"{settings.API_V1_PREFIX}/farms/terms/?farm_id={test_farm.id}&tid={test_term['id']}",
        headers=farm_terms_headers,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()


@farmOS_testing_server
def test_farm_terms_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/terms")
    assert r.status_code == 401
