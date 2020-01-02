from celery import Celery

from app.core.config import CELERY_WORKER_PING_INTERVAL

celery_app = Celery("worker", backend='rpc://', broker="amqp://guest@queue//", worker_send_task_events=True)

# Define the default timezone, user for scheduling.
celery_app.conf.timezone = 'UTC'

celery_app.conf.task_routes = {
    "app.worker.*": "main-queue",
}

# Add tasks to the celery beat schedule.
celery_app.conf.beat_schedule = {
    'ping-every-farm': {
        'task': 'app.worker.ping_farms',
        'schedule': CELERY_WORKER_PING_INTERVAL,
    },
}

