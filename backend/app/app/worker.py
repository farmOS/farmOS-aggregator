import logging

from raven import Client

from app.core.config import settings
from app.core.celery_app import celery_app
from app.db.session import Session
from app import crud
from app.api.utils.farms import get_farm_client

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task()
def ping_farms():
    db_session = Session()
    farm_list = crud.farm.get_multi(db_session)

    total_response = 0
    for farm in farm_list:
        try:
            farm_client = get_farm_client(db_session=db_session, farm=farm)
            info = farm_client.info()
            #logging.info("Farm: " + str(farm.id) + " version: " + info['api_version'])
            total_response += 1
        except Exception as e:
            continue

    db_session.close()
    return f"Pinged {total_response}/{len(farm_list)} farms."


@celery_app.task(bind=True)
def ping_farm(self, farm_id):
    db_session = Session()
    farm = crud.farm.get_by_id(db_session=db_session, farm_id=farm_id)

    if farm is not None:
        try:
            farm_client = get_farm_client(db_session=db_session, farm=farm)
            info = farm_client.info()
            return f"Success: pinged farm {farm_id}: {farm.farm_name}"

        except Exception as e:
            return f"Error: Can't connect to farm {farm_id}: {farm.farm_name}."
    else:
        return f"Error: farm {farm_id} does not exist"
