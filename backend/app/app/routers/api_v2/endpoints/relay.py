from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic.typing import Any, Optional
from requests import HTTPError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from app.routers.utils.db import get_db
from app.routers.utils.farms import ClientError, get_farm_by_url, get_farm_client
from app.schemas.farm import Farm

router = APIRouter()


# /farms/relay endpoint.


# TODO: This does not seem to work if the farm_url includes a http scheme.
# Specifying farm_url:path works, but then the second path:path argument does not accept a path.
# It seems that there can only be one path argument per route.
@router.api_route("/{farm_url}/{path:path}", methods=["GET", "POST", "PATCH", "DELETE"])
def relay(
    request: Request,
    response: Response,
    path: str,
    request_payload: Optional[Any] = Body(default=None),
    farm: Farm = Depends(get_farm_by_url),
    db: Session = Depends(get_db),
):
    # Get a farmOS client.
    try:
        farm_client = get_farm_client(db=db, farm=farm)
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail="Client error",
        )

    try:
        # Pass on a payload if provided.
        payload = None

        # If json was provided, pass the payload along under the json key.
        headers = {**request.headers}
        if "content-type" in headers and headers["content-type"] in [
            "application/json",
            "application/vnd.api+json",
        ]:
            payload = {"json": request_payload}
        elif request_payload:
            payload = request_payload

        # Relay the request.
        query_params = {**request.query_params}
        server_response = farm_client.session.http_request(
            path=path, method=request.method, options=payload, params=query_params
        )

        # Return the response.
        res_headers = server_response.headers
        response.status_code = server_response.status_code
        # Return json if specified.
        if "content-type" in res_headers and res_headers["content-type"] in [
            "application/json",
            "application/vnd.api+json",
        ]:
            return server_response.json()
        # For DELETE requests, return a new response object with no content.
        elif response.status_code == 204:
            return Response(status_code=204)
        # Else return the response content.
        else:
            return server_response.content

    except HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=str(e),
        )
