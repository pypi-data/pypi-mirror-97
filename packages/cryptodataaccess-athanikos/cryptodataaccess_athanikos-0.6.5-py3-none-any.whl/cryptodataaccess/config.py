import os
from keyring import get_password
from keyrings.alt.file import PlaintextKeyring
from werkzeug.utils import import_string
import keyring.backend

DB = "calculator_service"
PORT = 27017
LOCAL_SERVER = "127.0.0.1"
KAFKA_BROKERS = "134.122.79.43:9092"
CENTRAL_SERVER = "134.122.79.43"
CENTRAL_MONGO_DATABASE = "admin"
TRANSACTIONS_TOPIC_NAME = "transactions"
COMPUTED_NOTIFICATIONS_TOPIC_NAME = "computed_notifications"
USER_NOTIFICATIONS_TOPIC_NAME = "user_notifications"
LOCAL_MONGO_DATABASE = "admin"


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CENTRAL_SERVER = CENTRAL_SERVER
    CENTRAL_MONGO_DATABASE = CENTRAL_MONGO_DATABASE
    CENTRAL_MONGO_USERNAME = ""
    CENTRAL_MONGO_PASSWORD = ""
    CENTRAL_PORT = PORT
    LOCAL_PORT = PORT
    LOCAL_SERVER = LOCAL_SERVER
    LOCAL_MONGO_DATABASE = LOCAL_MONGO_DATABASE
    LOCAL_MONGO_USERNAME = ""
    LOCAL_MONGO_PASSWORD = ""
    LOGS_PATH = 'cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    COMPUTED_NOTIFICATIONS_TOPIC_NAME = COMPUTED_NOTIFICATIONS_TOPIC_NAME


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    CENTRAL_SERVER = CENTRAL_SERVER
    CENTRAL_MONGO_DATABASE = CENTRAL_MONGO_DATABASE
    CENTRAL_MONGO_USERNAME = ""
    CENTRAL_MONGO_PASSWORD = ""
    CENTRAL_PORT = PORT
    LOCAL_PORT = PORT
    LOCAL_SERVER = LOCAL_SERVER
    LOCAL_MONGO_DATABASE = LOCAL_MONGO_DATABASE
    LOCAL_MONGO_USERNAME = ""
    LOCAL_MONGO_PASSWORD = ""
    LOGS_PATH = 'cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    COMPUTED_NOTIFICATIONS_TOPIC_NAME = COMPUTED_NOTIFICATIONS_TOPIC_NAME


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    CENTRAL_SERVER = CENTRAL_SERVER
    CENTRAL_MONGO_DATABASE = CENTRAL_MONGO_DATABASE
    CENTRAL_MONGO_USERNAME = ""
    CENTRAL_MONGO_PASSWORD = ""
    CENTRAL_PORT = PORT
    LOCAL_PORT = PORT
    LOCAL_SERVER = LOCAL_SERVER
    LOCAL_MONGO_DATABASE = LOCAL_MONGO_DATABASE
    LOCAL_MONGO_USERNAME = ""
    LOCAL_MONGO_PASSWORD = ""
    LOGS_PATH = 'cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    COMPUTED_NOTIFICATIONS_TOPIC_NAME = COMPUTED_NOTIFICATIONS_TOPIC_NAME


config = {
    "development": "cryptodataaccess.config.DevelopmentConfig",
    "production": "cryptodataaccess.config.ProductionConfig",
    "default": "cryptodataaccess.config.DevelopmentConfig",
}


def configure_app():
    keyring.set_keyring(PlaintextKeyring())
    config_name = os.getenv('FLASK_ENV', 'cryptodataaccess.config.DevelopmentConfig')
    cfg = import_string(config_name)()
    cfg.LOCAL_MONGO_USERNAME = get_password('cryptodataaccess', 'LOCAL_MONGO_USERNAME')
    cfg.LOCAL_MONGO_PASSWORD = get_password('cryptodataaccess', cfg.LOCAL_MONGO_USERNAME)
    cfg.CENTRAL_MONGO_USERNAME = get_password('cryptodataaccess', 'CENTRAL_MONGO_USERNAME')
    cfg.CENTRAL_MONGO_PASSWORD = get_password('cryptodataaccess', cfg.CENTRAL_MONGO_USERNAME)
    return cfg

