import mock
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError
from cryptomodel.cryptostore import user_channel, user_notification
from cryptomodel.coinmarket import prices
from cryptomodel.fixer import exchange_rates
from cryptodataaccess.config import configure_app
from cryptodataaccess.Users.UsersRepository import UsersRepository
from cryptodataaccess.Rates.RatesRepository import RatesRepository
import pytest
from cryptodataaccess.helpers import do_local_connect
from cryptodataaccess.tests.helpers import insert_prices_record, insert_exchange_record


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_fetch_symbol_rates():
    config = configure_app()
    repo = RatesRepository(config, mock_log)
    do_local_connect(config)
    prices.objects.all().delete()
    insert_prices_record()
    objs = repo.fetch_symbol_rates()
    assert (len(objs.rates) == 100)
    assert (objs.rates['BTC'].price == 8101.799293468747)


def test_fetch_exchange_rates():
    config = configure_app()
    repo = RatesRepository(config, mock_log)
    do_local_connect(config)
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
    repo = RatesRepository(config, mock_log)
    do_local_connect(config)
    prices.objects.all().delete()
    insert_prices_record()
    objs = repo.fetch_latest_prices_to_date('2020-07-03')  # bound case : timestamp is saved as string so it cant find
    # it because  of the time stuff (either+1 day?)
    assert (len(objs) == 0)
    objs = repo.fetch_latest_prices_to_date('2020-07-04')
    assert (len(objs) == 1)
    symbols = repo.fetch_symbols()
    assert (len(symbols) == 100)


def test_insert_user_channel():
    config = configure_app()
    repo = UsersRepository(config, mock_log)
    do_local_connect(config)
    user_channel.objects.all().delete()
    uc = repo.add_user_channel(1, 'da', '1')
    assert (uc.channel_type == 'da')


def test_log_when_do_connect_raises_exception(mock_log):
    with mock.patch("cryptodataaccess.helpers.do_connect"
                    ) as _mock:
        _mock.side_effect = ServerSelectionTimeoutError("hi")
        with mock.patch("cryptodataaccess.helpers.log_error") as log:
            with pytest.raises(ServerSelectionTimeoutError):
                repo = UsersRepository(configure_app(), mock_log)
                repo.add_user_channel(1, "telegram", chat_id="1")
            mock_log.assert_called()


def test_update_notification_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = UsersRepository(config, mock_log)
    do_local_connect(config)
    user_notification.objects.all().delete()
    with pytest.raises(ValueError):
        repo.edit_notification(ObjectId('666f6f2d6261722d71757578'), 1, 'nik2', 'email', 'some expr', 1, 1, True, 'telegram', 'expr to send', ObjectId('666f6f2d6261722d71757578'), 'Modified')


def test_update_notification():
    config = configure_app()
    repo = UsersRepository(config, mock_log)
    do_local_connect(config)
    user_notification.objects.all().delete()
    un = repo.add_notification(1, 'username', 'email', 'some expr', 1, 1, True, 'telegram', 'expr to send', ObjectId('666f6f2d6261722d71757578'), 'Added')
    un = repo.edit_notification(un.id, 1, 'nik2', 'email', 'some expr', 1, 1, True, 'telegram', 'expr to send', ObjectId('666f6f2d6261722d71757578'), 'Modified')
    assert (un.user_name == "nik2")


def test_delete_notification_when_exists():
    config = configure_app()
    repo = UsersRepository(config, mock_log)
    do_local_connect(config)
    user_notification.objects.all().delete()
    ut = repo.add_notification(1, 'username', 'email', 'some expr', 1, 1, True, 'telegram', 'expr to send', ObjectId('666f6f2d6261722d71757578'), 'Added')
    assert (len(user_notification.objects) == 1)
    ut = repo.remove_notification(ut.id)
    assert (len(user_notification.objects) == 0)
