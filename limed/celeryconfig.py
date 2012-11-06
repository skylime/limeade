import os
import sys
sys.path.insert(0, os.getcwd())

CELERY_IMPORTS = ("cloud", "mysql")

# BROKER_URL = "transport://userid:password@hostname:port/virtual_host"
BROKER_URL = "amqp://limeade:secret@localhost:5672/limeade"

CELERY_RESULT_BACKEND = "amqp"

TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_QUEUES = {
    'celery': {'binding_key': 'celery'},
    'limeade.cloud': {'binding_key': 'limeade.cloud'},
    'limeade.mysql': {'binding_key': 'limeade.mysql'},
}
