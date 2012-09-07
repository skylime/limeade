import os
import sys
sys.path.insert(0, os.getcwd())

CELERY_IMPORTS = ("cloud", "mysql")

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "limeade"
BROKER_PASSWORD = "EimequuChuap8aa8ohyo"
BROKER_VHOST = "limeade"

CELERY_RESULT_BACKEND = "amqp"

TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_QUEUES = {
    'celery': {'binding_key': 'celery'},
    'limeade.cloud': {'binding_key': 'limeade.cloud'},
    'limeade.mysql': {'binding_key': 'limeade.mysql'},
}
