from datetime import datetime

import mock
from bson import ObjectId
from cryptomodel.operations import OPERATIONS
from cryptomodel.cryptostore import user_channel, user_notification, user_settings
from cryptomodel.coinmarket import prices
from cryptomodel.fixer import exchange_rates

from cryptodataaccess.Memory import USER_NOTIFICATIONS_MEMORY_KEY, USER_SETTINGS_MEMORY_KEY, USER_CHANNELS_MEMORY_KEY
from cryptodataaccess.Rates.RatesMongoStore import RatesMongoStore
from cryptodataaccess.Users.UsersMongoStore import UsersMongoStore
from cryptodataaccess.config import configure_app
from cryptodataaccess.Users.UsersRepository import UsersRepository
from cryptodataaccess.Rates.RatesRepository import RatesRepository
import pytest

from cryptodataaccess.helpers import convert_to_int_timestamp
from cryptodataaccess.tests.helpers import insert_prices_record, insert_exchange_record
from cryptodataaccess import helpers


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_fetch_symbol_rates():
    config = configure_app()
    rates_store = RatesMongoStore(config, mock_log)
    repo = RatesRepository(rates_store)

    helpers.do_local_connect(config)
    prices.objects.all().delete()
    insert_prices_record()
    objs = repo.fetch_symbol_rates()
    assert (len(objs.rates) == 100)
    assert (objs.rates['BTC'].price == 8101.799293468747)


def test_fetch_exchange_rates():
    config = configure_app()
    rates_store = RatesMongoStore(config, mock_log)
    repo = RatesRepository(rates_store)

    exchange_rates.objects.all().delete()
    insert_exchange_record()
    objs = repo.fetch_latest_exchange_rates_to_date('1900-01-01')
    assert (len(objs) == 0)
    objs = repo.fetch_latest_exchange_rates_to_date('2020-07-04')
    assert (len(objs) == 1)
    objs = repo.fetch_latest_exchange_rates_to_date('2020-07-03')
    assert (len(objs) == 1)
    assert (objs[0].rates.AED == 4.127332)
    objs = repo.fetch_latest_exchange_rates_to_date('2020-07-02')
    assert (len(objs) == 0)


def test_fetch_prices_and_symbols():
    config = configure_app()
    rates_store = RatesMongoStore(config, mock_log)
    repo = RatesRepository(rates_store)

    prices.objects.all().delete()
    insert_prices_record()

    dt = convert_to_int_timestamp(datetime(year=2020, month=7, day=3))
    objs = repo.fetch_latest_prices_to_date(dt)
    assert (len(objs) == 1)
    objs = repo.fetch_latest_prices_to_date(dt)

    dt = convert_to_int_timestamp(datetime(year=2020, month=7, day=4))

    assert (len(objs) == 1)
    symbols = repo.fetch_symbols()
    assert (len(symbols) == 100)


def test_insert_user_channel():
    config = configure_app()
    rates_store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(rates_store)
    helpers.do_local_connect(config)

    user_channel.objects.all().delete()
    repo.add_user_channel(user_id=1, chat_id='1', channel_type='telegram',
                          source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    uc = repo.memories[USER_CHANNELS_MEMORY_KEY].items[0]
    assert (uc.channel_type == 'telegram')
    assert (uc.operation == OPERATIONS.ADDED.name)


def test_insert_user_setting():
    config = configure_app()
    users_store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(users_store)
    helpers.do_local_connect(config)
    user_settings.objects.all().delete()
    repo.add_user_settings(user_id=1, preferred_currency='da', source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    uc = repo.memories[USER_SETTINGS_MEMORY_KEY].items[0]
    assert (uc.preferred_currency == 'da')
    assert (uc.operation == OPERATIONS.ADDED.name)


def test_update_notification_when_does_not_exist_throws_ValueError():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    helpers.do_local_connect(config)

    user_notification.objects.all().delete()
    with pytest.raises(ValueError):
        repo.edit_notification(
            in_id=ObjectId('666f6f2d6261722d71757578'),
            channel_type="TELEGRAM",
            notification_type="BALANCE",
            user_id=1,
            user_name="test",
            user_email="ds",
            is_active=False,
            source_id=ObjectId('666f6f2d6261722d71757578'),
            check_every="00:00",
            start_date=datetime.now(),
            end_date=datetime.now(),
            threshold_value=1

        )
        repo.commit()


def test_update_notification():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    helpers.do_local_connect(config)

    user_notification.objects.all().delete()
    repo.add_notification(user_id=1, user_name='username', user_email='email',
                          notification_type='BALANCE',
                          is_active=True, channel_type='TELEGRAM',
                          threshold_value=1,
                          check_every="00:00",
                          start_date=datetime.now(),
                          end_date=datetime.now(),
                          source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    un = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]

    repo.edit_notification(in_id=un.id,
                           user_id=1, user_name='username2', user_email='email',
                           notification_type='BALANCE', check_every="00:00",
                           start_date=datetime.now(),
                           end_date=datetime.now(),
                           is_active=True, channel_type='TELEGRAM',
                           threshold_value=1,
                           source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    un = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]

    assert (un.user_name == "username2")
    repo.edit_notification(in_id=un.id,
                           user_id=1, user_name='username2', user_email='email',
                           notification_type='BALANCE', check_every="00:00",
                           start_date=datetime.now(),
                           end_date=datetime.now(),
                           is_active=True, channel_type='TELEGRAM',
                           threshold_value=1,
                           source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    un = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]


def test_delete_notification_when_exists():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    helpers.do_local_connect(config)

    user_notification.objects.all().delete()

    repo.add_notification(user_id=1, user_name='username', user_email='email',
                          threshold_value=1,
                          notification_type="BALANCE",
                          check_every="00:00",
                          start_date=datetime.now(),
                          end_date=datetime.now(),

                          is_active=True, channel_type='TELEGRAM', source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    ut = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]

    assert (len(user_notification.objects) == 1)
    ut = repo.remove_notification(ut.id)
    repo.commit()
    assert (len(user_notification.objects) == 0)


def test_fetch_notification_when_exists():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)
    helpers.do_local_connect(config)

    user_notification.objects.all().delete()

    repo.add_notification(user_id=1, user_name='username', user_email='email',
                          threshold_value=1,
                          notification_type="BALANCE",
                          check_every="00:00",
                          start_date=datetime.now(),
                          end_date=datetime.now(),

                          is_active=True, channel_type='TELEGRAM', source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()

    ut = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]

    ut = repo.get_notification(ut.id)[0]

    assert (ut.notification_type == "BALANCE")
    assert (ut.user_name == "username")


def test_fetch_notification_when_does_not_exists():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)
    helpers.do_local_connect(config)

    user_notification.objects.all().delete()

    ut = repo.get_notification(ObjectId('666f6f2d6261722d71757578'))

    assert (len(ut) == 0)


def test_delete_user_notification_when_exists_by_source_id():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    helpers.do_local_connect(config)

    user_notification.objects.all().delete()

    repo.add_notification(user_id=1, user_name='username', user_email='email',
                          expression_to_evaluate='some expr', check_every_seconds=1, check_times=1,
                          is_active=True, channel_type='telegram',
                          fields_to_send="dsd",
                          source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    ut = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]
    assert (len(user_notification.objects) == 1)
    store.do_delete_user_notification_by_source_id(source_id=ObjectId('666f6f2d6261722d71757578'))
    assert (len(user_notification.objects) == 0)


def test_delete_user_notification_when_exists_by_source_id():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    helpers.do_local_connect(config)

    user_notification.objects.all().delete()

    repo.add_notification(user_id=1, user_name='username', user_email='email',
                          notification_type='BALANCE',
                          is_active=True, channel_type='TELEGRAM',
                          threshold_value=1,
                          check_every="00:00",
                          start_date=datetime.now(),
                          end_date=datetime.now(),
                          source_id=ObjectId('666f6f2d6261722d71757578'))
    repo.commit()
    ut = repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items[0]
    assert (len(user_notification.objects) == 1)
    store.do_delete_user_notification_by_source_id(source_id=ObjectId('666f6f2d6261722d71757578'))
    assert (len(user_notification.objects) == 0)


def test_Users_Repository_create():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)

    assert (repo.memories[USER_NOTIFICATIONS_MEMORY_KEY] is not None)
    assert (repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items is not None)


def test_do_delete_notification_when_does_not_exist_should_not_throw():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)

    noti = user_notification()
    noti.id = ObjectId('666f6f2d6261722d71757578')
    noti.source_id = ObjectId('666f6f2d6261722d71757578')
    store.delete_notification(notification=noti, throw_if_does_not_exist=False)
    assert (1 == 1)


def test_remove_notification_by_source_id_should_not_add_any_object_to_memory_when_does_not_exist_in_db_and_mem():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)
    helpers.do_local_connect(config)
    user_notification.objects.all().delete()

    store.do_delete_user_notification_by_source_id(source_id=ObjectId('666f6f2d6261722d71757578'),
                                                   throw_if_does_not_exist=False)
    assert (len(repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items) == 0)


def test_delete_notification_by_source_id_should_not_add_any_object_to_memory_when_does_not_exist_in_db_and_mem():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)
    helpers.do_local_connect(config)
    user_notification.objects.all().delete()

    store.do_delete_user_notification_by_source_id(source_id=ObjectId('666f6f2d6261722d71757578'),
                                                   throw_if_does_not_exist=False)
    assert (len(repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items) == 0)


def test_remove_notification_by_source_id_should_not_add_any_object_to_memory_when_does_not_exist_in_db_and_mem():
    config = configure_app()
    store = UsersMongoStore(config, mock_log)
    repo = UsersRepository(store)
    helpers.do_local_connect(config)
    user_notification.objects.all().delete()

    repo.remove_notification_by_source_id(source_id=ObjectId('666f6f2d6261722d71757578'))
    assert (len(repo.memories[USER_NOTIFICATIONS_MEMORY_KEY].items) == 0)
