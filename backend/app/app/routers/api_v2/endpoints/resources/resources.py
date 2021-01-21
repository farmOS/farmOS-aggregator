from fastapi import APIRouter, Depends, Query
from starlette.requests import Request
from pydantic import BaseModel
from pydantic.typing import Dict, List, Optional, Union, Any
from sqlalchemy.orm import Session

from app.routers.utils.db import get_db
from app.routers.utils.farms import get_active_farms_url_or_list, get_farm_client, ClientError
from app.schemas.farm import Farm

router = APIRouter()

# /farms/resources endpoint.


# todo: Use pydantic.types.UUID4 instead of string for IDs once farmOS.py supports this.
class ResourceIdentifier(BaseModel):
    id: Optional[str]
    type: Optional[str]


class Relationship(BaseModel):
    data: List[Optional[ResourceIdentifier]]


class Resource(BaseModel):
    id: Optional[str]
    type: Optional[str]
    attributes: Optional[Dict[str, Union[Any]]]
    relationships: Optional[Dict[str, Relationship]]


class ResourceUpdate(Resource):
    id: str


@router.get("/{entity_type}/{bundle}")
def get_resource(
    request: Request,
    entity_type: str,
    bundle: str,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    query_params = {**request.query_params}
    query_params.pop('farm_id', None)
    query_params.pop('farm_url', None)

    data = {}
    for farm in farm_list:
        data[farm.id] = None

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError as e:
            data[farm.id] = str(e)
            continue

        # Make the request.
        try:
            response = farm_client.resource.get(entity_type, bundle, query_params)
            data[farm.id] = response
        except Exception as e:
            data[farm.id] = str(e)
            continue

    return data


@router.post("/{entity_type}/{bundle}")
def create_resource(
    resource: Resource,
    entity_type: str,
    bundle: str,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError as e:
            data[farm.id] = str(e)
            continue

        # Make the request.
        try:
            data[farm.id] = farm_client.resource.send(entity_type, bundle, payload=resource.dict(exclude_unset=True))
        except Exception as e:
            data[farm.id] = str(e)
            continue

    return data


@router.put("/{entity_type}/{bundle}")
def update_resource(
    resource: ResourceUpdate,
    entity_type: str,
    bundle: str,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError as e:
            data[farm.id] = str(e)
            continue

        # Make the request.
        try:
            data[farm.id] = farm_client.resource.send(entity_type, bundle, payload=resource.dict(exclude_unset=True))
        except Exception as e:
            data[farm.id] = str(e)
            continue

    return data


@router.delete("/{entity_type}/{bundle}")
def delete_farm_assets(
    entity_type: str,
    bundle: str,
    id: List[str] = Query(None),
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError:
            data[farm.id] = str(e)
            continue

        # Make the request.
        for single_id in id:
            try:
                response = farm_client.resource.delete(entity_type, bundle, id=single_id)
                data[farm.id].append({single_id: response})
            except Exception as e:
                data[farm.id].append({single_id: str(e)})
                continue

    return data
