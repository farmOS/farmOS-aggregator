import pytest
from farmOS.client_2 import ResourceBase
from fastapi.testclient import TestClient
from requests.sessions import Session

from app.schemas.api_key import ApiKeyCreate
from app.tests.utils.utils import farmOS_testing_server, get_api_key_headers


class AggregatorSession(Session):
    def __init__(self, hostname, api_key, farm_id):
        super().__init__()
        self.hostname = hostname
        self.farm_id = farm_id
        self._content_type = "application/vnd.api+json"
        self.headers.update({"api-key": api_key})

    def http_request(self, path, method="GET", options=None, params=None, headers=None):
        # Strip protocol, hostname, leading/trailing slashes, and whitespace from the path.
        path = path.strip("/")
        path = path.strip()

        return self._http_request(
            url=path, method=method, options=options, params=params, headers=headers
        )

    def _http_request(self, url, method="GET", options=None, params=None, headers=None):

        url = f"{self.hostname}/api/v2/farms/relay/{url}"

        if params is None:
            params = {}

        params["farm_id"] = self.farm_id

        # Automatically follow redirects, unless this is a POST request.
        # The Python requests library converts POST to GET during a redirect.
        # Allow this to be overridden in options.
        allow_redirects = True
        if method in ["POST", "PUT"]:
            allow_redirects = False
        if options and "allow_redirects" in options:
            allow_redirects = options["allow_redirects"]

        if headers is None:
            headers = {}

        # If there is data to be sent, include it.
        data = None
        if options and "data" in options:
            data = options["data"]
            headers["Content-Type"] = self._content_type

        # If there is a json data to be sent, include it.
        json = None
        if options and "json" in options:
            json = options["json"]
            if "Content-Type" not in headers:
                headers["Content-Type"] = self._content_type

        # Perform the request.
        response = self.request(
            method,
            url,
            headers=headers,
            allow_redirects=allow_redirects,
            data=data,
            json=json,
            params=params,
        )

        # If this is a POST request, and a redirect occurred, attempt to re-POST.
        redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
        if method in ["POST", "PUT"] and response.status_code in redirect_codes:
            if response.headers["Location"]:
                response = self.request(
                    method,
                    response.headers["Location"],
                    allow_redirects=True,
                    data=data,
                    json=json,
                    params=params,
                )

        # Raise exception if error.
        response.raise_for_status()

        # Return the response.
        return response


@pytest.fixture
def resources_api(client: TestClient, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key", enabled=True, all_farms=True, scopes=["farm:read"]
    )
    headers = get_api_key_headers(client=client, api_key_params=test_api_key)

    hostname = "http://localhost"
    session = AggregatorSession(hostname, headers["api-key"], test_farm.id)
    resources = ResourceBase(session)
    return resources


@farmOS_testing_server
def test_relay_crud_activity_logs(resources_api):
    # Create a log.
    test_log = {
        "attributes": {"name": "Test Log from farmOS-aggregator", "status": "done"},
    }
    response = resources_api.send("log", "activity", test_log)

    # Check log was created
    assert "data" in response
    test_farm_log = response["data"]
    assert "id" in test_farm_log
    created_log_id = test_farm_log["id"]
    test_log["id"] = created_log_id

    # Test a GET with the log ID.
    response = resources_api.get_id("log", "activity", test_log["id"])

    # Check attributes
    assert "data" in response
    created_log = response["data"]
    assert created_log["type"] == test_log["type"]
    assert created_log["attributes"]["name"] == test_log["attributes"]["name"]

    # Change log attributes
    test_log["attributes"]["name"] = "Updated name from farmOS-aggregator"
    test_log["attributes"]["status"] = "pending"
    test_log = test_log
    response = resources_api.send("log", "activity", test_log)

    # Check response
    assert "data" in response
    updated_log = response["data"]
    assert updated_log["attributes"]["name"] == test_log["attributes"]["name"]

    # Delete log
    response = resources_api.delete("log", "activity", updated_log["id"])
    assert response.status_code == 204
