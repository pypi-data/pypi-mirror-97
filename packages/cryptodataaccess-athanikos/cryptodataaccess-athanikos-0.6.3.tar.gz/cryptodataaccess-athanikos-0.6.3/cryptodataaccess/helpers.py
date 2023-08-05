import mongoengine
from mongoengine import connect, Q
from pymongo.errors import ServerSelectionTimeoutError
import logging


def do_local_connect(configuration):
    url = 'mongodb://' + configuration.LOCAL_MONGO_USERNAME + ':' + configuration.LOCAL_MONGO_PASSWORD + '@' \
          + configuration.LOCAL_SERVER + ':' + str(configuration.LOCAL_PORT) + '/?authSource=admin'
    local_conn = connect(db=configuration.LOCAL_MONGO_DATABASE, username=configuration.LOCAL_MONGO_USERNAME, host=url)


def do_central_connect(configuration):
    url = 'mongodb://' + configuration.CENTRAL_MONGO_USERNAME + ':' + configuration.CENTRAL_MONGO_PASSWORD + '@' \
          + configuration.CENTRAL_SERVER + ':' + str(configuration.CENTRAL_PORT) + '/?authSource=admin'
    central_conn = connect(db=configuration.CENTRAL_MONGO_DATABASE, username=configuration.CENTRAL_MONGO_USERNAME, host=url)


def get_local_url(configuration):
    return 'mongodb://' + configuration.LOCAL_MONGO_USERNAME + ':' + configuration.LOCAL_MONGO_PASSWORD + '@' \
           + configuration.LOCAL_SERVER + ':' + str(configuration.LOCAL_PORT) + '/?authSource=admin'


def get_central_url(configuration):
    return 'mongodb://' + configuration.CENTRAL_MONGO_USERNAME + ':' + configuration.CENTRAL_MONGO_PASSWORD + '@' \
           + configuration.CENTRAL_SERVER + ':' + str(configuration.CENTRAL_PORT) + '/?authSource=admin'



def server_time_out_wrapper(repository, method_to_call, *args):
    try:
        return method_to_call(*args)
    except ServerSelectionTimeoutError as inst:
        repository.log_error(exception=inst, web_method_name=str(method_to_call), cfg=repository.configuration)
        raise
    except mongoengine.connection.ConnectionFailure as cf:
        repository.log_error(exception=cf, web_method_name=str(method_to_call), cfg=repository.configuration)
        raise mongoengine.connection.ConnectionFailure(cf)


def convert_to_int_timestamp(dt):
    return int(dt.timestamp()) * 1000


def if_none_raise_with_id(_id, trans):
    if trans is None:
        raise ValueError(str(_id) + " does not exist ")


def if_none_raise(trans):
    if trans is None:
        raise ValueError(" does not exist ")


def if_empty_string_raise(value):
    if value is None:
        raise ValueError(" does not exist ")
    if value == '':
        raise ValueError(" does not exist ")


def log_error(exception, pk_id, web_method_name, cfg):
    logging.basicConfig(filename=cfg.LOGS_PATH, level=logging.ERROR)
    logging.error(str(pk_id) + ' ' + str(web_method_name) + ' ' + str(exception))
