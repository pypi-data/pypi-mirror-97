from datetime import datetime

import mock
from cryptomodel.coinmarket import prices
from cryptomodel.cryptomodel import user_transaction, exchange_rates

from cryptodataaccess.Rates.RatesMongoStore import RatesMongoStore
from cryptodataaccess.Rates.RatesRepository import RatesRepository
from cryptodataaccess.config import configure_app
import pytest
from cryptodataaccess.helpers import do_local_connect, convert_to_int_timestamp
from cryptodataaccess.tests.helpers import insert_prices_record, insert_exchange_record, insert_prices_record_with_method, \
    get_prices20200812039_record, get_prices20200801T2139_record

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_fetch_symbol_rates_for_date_pass_str_or_dt():
    config = configure_app()
    do_local_connect(config)
    user_transaction.objects.all().delete()
    exchange_rates.objects.all().delete()
    prices.objects.all().delete()

    insert_prices_record()
    insert_exchange_record()

    config = configure_app()
    store = RatesMongoStore(config, mock_log)
    rates_repo = RatesRepository(store)
    do_local_connect(config)

    rates_repo.fetch_symbol_rates_for_date(convert_to_int_timestamp(datetime.today()))

    dt = datetime(year=2040, month=1, day=1)
    rates_repo.fetch_symbol_rates_for_date(convert_to_int_timestamp(dt))

    assert (len(prices.objects) == 1)


def test_fetch_symbol_rates_for_dat_with_two_entries_within_two_hours():
    config = configure_app()
    users_store = RatesMongoStore(config, mock_log)
    rates_repo = RatesRepository(users_store)
    do_local_connect(config)
    dt_now = convert_to_int_timestamp(datetime.today())
    user_transaction.objects.all().delete()
    prices.objects.all().delete()

    insert_exchange_record()
    insert_prices_record_with_method(get_prices20200812039_record)
    insert_prices_record_with_method(get_prices20200801T2139_record)
    rts = rates_repo.fetch_symbol_rates_for_date(convert_to_int_timestamp(datetime.today()))
    dt = datetime(year=2020, month=8, day=1, hour=21, minute=0) #1596304800
    print(dt.timestamp()) #

    # assert (rts.rates['BTC'].last_updated == '2020-08-01T21:38:00.000Z')

    # dt = datetime(year=2020, month=8 , day=1, hour=21, minute=0 )
    # rts =      rates_repo.fetch_symbol_rates_for_date(convert_to_int_timestamp(dt))
    # assert(rts.rates['BTC'].last_updated =='2013-04-28T00:00:00.000Z' )
