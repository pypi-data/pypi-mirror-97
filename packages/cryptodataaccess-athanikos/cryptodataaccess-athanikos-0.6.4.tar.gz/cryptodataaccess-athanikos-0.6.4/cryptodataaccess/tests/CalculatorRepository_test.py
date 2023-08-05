from datetime import datetime

import mock
from bson import ObjectId
from cryptomodel.computed_notification import computed_notification
from cryptomodel.operations import OPERATIONS
from cryptomodel.cryptostore import user_channel, user_notification, user_settings
from cryptomodel.coinmarket import prices
from cryptomodel.fixer import exchange_rates

from cryptodataaccess.Calculator.CalculatorMongoStore import CalculatorMongoStore
from cryptodataaccess.Calculator.CalculatorRepository import CalculatorRepository
from cryptodataaccess.Memory import USER_NOTIFICATIONS_MEMORY_KEY, USER_SETTINGS_MEMORY_KEY, USER_CHANNELS_MEMORY_KEY, \
    CALCULATOR_MEMORY_KEY
from cryptodataaccess.Rates.RatesMongoStore import RatesMongoStore
from cryptodataaccess.Users.UsersMongoStore import UsersMongoStore
from cryptodataaccess.config import configure_app
from cryptodataaccess.Users.UsersRepository import UsersRepository
from cryptodataaccess.Rates.RatesRepository import RatesRepository
import pytest

from cryptodataaccess.helpers import do_local_connect


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_insert_computed_notification():
    config = configure_app()
    store = CalculatorMongoStore(config, mock_log)
    repo = CalculatorRepository(store)
    do_local_connect(config)
    computed_notification.objects.all().delete()
    ut = repo.add_computed_notification(user_id=1,user_name="ds",user_email="ds",
                                        notification_type="BALANCE",check_every="00:01",
                                        is_active=True,
                                        computed_date="2020-01-01",
                                        end_date="2020-01-01",
                                        start_date="2020-01-01",
                                        threshold_value=1,channel_type="TELEGRAM",
                                        result="sss",
                                        source_id=ObjectId('666f6f2d6261722d71757578')

                                        )
    repo.commit()

    cn = repo.memories[CALCULATOR_MEMORY_KEY].items[0]
    assert (cn.user_id == 1)
    assert (len(computed_notification.objects) == 1)
    assert (cn.operation == OPERATIONS.ADDED.name)


    ut = repo.add_computed_notification(user_id=1,user_name="ds",user_email="ds",
                                        notification_type="BALANCE",check_every="00:01",
                                        is_active=True,
                                        computed_date="2020-01-01",
                                        end_date="2020-01-01",
                                        start_date="2020-01-01",
                                        threshold_value=1,channel_type="TELEGRAM",
                                        result="sss",
                                        source_id=ObjectId('666f6f2d6261722d71757578')

                                        )
    repo.commit()
    cn = repo.memories[CALCULATOR_MEMORY_KEY].items[0]
    assert (cn.user_id == 1)
    assert (len(computed_notification.objects) == 2)
    assert (cn.operation == OPERATIONS.ADDED.name)
