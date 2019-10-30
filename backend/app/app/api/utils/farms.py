from functools import partial
from farmOS import farmOS
from farmOS.config import ClientConfig

from app import crud
from app.models.farm_token import FarmTokenBase
from app.crud.farm_token import create_farm_token, update_farm_token
from app.models.farm import FarmUpdate


def get_farm_list(
        db,
        farm_id=None,
        farm_id_list=None,
        farm_url=None,
        get_all=True,
        skip=0,
        limit=100
    ):
    farm_list = []

    if farm_id is not None:
        farm = crud.farm.get_by_id(db, farm_id=farm_id)
        if farm is not None:
            farm_list.append(farm)

    if farm_id_list is not None:
        farms = crud.farm.get_by_multi_id(db, farm_id_list=farm_id_list)
        if farms is not None:
            farm_list.extend(farms)

    if farm_url is not None:
        farm = crud.farm.get_by_url(db, farm_url=farm_url)
        if farm is not None:
            farm_list.append(farm)

    if get_all and not farm_url and not farm_id_list and not farm_id:
        farms = crud.farm.get_multi(db, skip=skip, limit=limit)
        if farms is not None:
            farm_list.extend(farms)

    return farm_list


# A helper function to save OAuth Tokens to DB.
def _save_token(token, db_session=None, farm=None):
    token_in = FarmTokenBase(farm_id=farm.id, **token)

    # Make sure we have a DB session and Farm object.
    if db_session is not None and farm is not None:
        # Update the farm token if it exists.
        if farm.token is not None:
            update_farm_token(db_session, farm.token, token_in)
        else:
            create_farm_token(db_session, token_in)


# Create a farmOS.py client.
def get_farm_client(db_session, farm):
    client_id = 'farmos_api_client'
    client_secret = 'client_secret'

    config = ClientConfig()

    config_values = {
        'Profile': {
            'development': 'True',
            'hostname': farm.url,
            'username': farm.username,
            'password': farm.password,
            'client_id': client_id,
            'client_secret': client_secret,
        }
    }

    if farm.token is not None:
        config_values['Profile']['access_token'] = farm.token.access_token
        config_values['Profile']['refresh_token'] = farm.token.refresh_token
        config_values['Profile']['expires_at'] = farm.token.expires_at
    config.read_dict(config_values)

    token_updater = partial(_save_token, db_session=db_session, farm=farm)

    try:
        client = farmOS(config=config, profile_name="Profile", token_updater=token_updater)
    except Exception as e:
        crud.farm.update(db_session, farm=farm, farm_in=FarmUpdate(is_authorized=False))
        raise ClientError(e)

    crud.farm.update(db_session, farm=farm, farm_in=FarmUpdate(is_authorized=True))

    return client


class ClientError(Exception):
    def __init__(self, message):
        self.message = message