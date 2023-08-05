from datetime import datetime

import mock
from bson import ObjectId
from cryptomodel.cryptostore import user_transaction
from cryptomodel.operations import OPERATIONS

from cryptodataaccess.Memory import TRANSACTIONS_MEMORY_KEY
from cryptodataaccess.Transactions.TransactionMongoStore import TransactionMongoStore
from cryptodataaccess.config import configure_app
from cryptodataaccess.Transactions.TransactionRepository import TransactionRepository
import pytest
from cryptodataaccess.helpers import do_local_connect
from mongoengine import Q


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_insert_transaction():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                              source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[0]
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT")
    assert (len(user_transaction.objects) == 1)
    assert (ut.operation == OPERATIONS.ADDED.name)


def test_update_transaction():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")

    assert (len(repo.memories) == 1)
    assert (len(repo.memories[TRANSACTIONS_MEMORY_KEY].items) == 1)

    repo.commit()
    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[0]

    repo.edit_transaction(ut.id, 1, 1, 'OXT2', 1, 1, "EUR", "2020-01-01", "kraken",
                          source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[1]

    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT2")
    assert (ut.currency == "EUR")
    assert (ut.operation == OPERATIONS.MODIFIED.name)


def test_update_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    with pytest.raises(ValueError):
        repo.edit_transaction(ObjectId('666f6f2d6261722d71757578'), 1, 1, 'OXT', "EUR", 1, 1, "2020-01-01",
                              "kraken", source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
        repo.commit()

def test_delete_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    trans = user_transaction()
    trans.id = ObjectId('666f6f2d6261722d71757578')
    with pytest.raises(ValueError):
        store.delete_transaction(trans, True)


def test_delete_transaction_when_does_not_exist_and_throw_is_false_does_not_throw():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    trans = user_transaction()
    trans.id = ObjectId('666f6f2d6261722d71757578')
    store.delete_transaction(trans, False)


def test_delete_transaction_when_exists():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    repo.add_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    assert (len(user_transaction.objects) == 1)

    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[0]

    repo.remove_transaction(ut.id)
    repo.commit()

    assert (len(user_transaction.objects) == 0)


def test_delete_transaction_when_exists_by_source_id():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()

    ut = repo.add_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken",
                              source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    assert (len(user_transaction.objects) == 1)
    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[0]
    repo.remove_transaction_by_source_id(source_id=ut.source_id)
    repo.commit()
    assert (len(user_transaction.objects) == 0)


def test_fetch_transaction():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                              source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()

    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[0]
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT")
    assert (ut.currency == "USD")
    assert (ut.operation == OPERATIONS.ADDED.name)
    assert (ut.source_id == ObjectId('666f6f2d6261722d71757578'))
    repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=None, transaction_type="TRADE", order_type="BUY")
    repo.commit()
    ut = repo.memories[TRANSACTIONS_MEMORY_KEY].items[1]
    ut = repo.get_transaction(ut.id)
    assert (ut.source_id is None)


def test_fetch_distinct_user_ids():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()
    repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")

    repo.commit()
    items = repo.get_distinct_user_ids()
    assert (len(items) == 1)
    user_transaction.objects.all().delete()
    repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.add_transaction(12, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")

    repo.commit()
    items = repo.get_distinct_user_ids()
    assert (len(items) == 2)
    user_transaction.objects.all().delete()
    repo.add_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.add_transaction(12, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.add_transaction(3, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.add_transaction(122, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                         source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    items = repo.get_distinct_user_ids()
    assert (len(items) == 4)


def test_get_transaction_by_date():
    config = configure_app()
    store = TransactionMongoStore(config, mock_log)
    repo = TransactionRepository(store)
    do_local_connect(config)
    user_transaction.objects.all().delete()

    repo.add_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken",
                              source_id=ObjectId('666f6f2d6261722d71757578'), transaction_type="TRADE", order_type="BUY")
    repo.commit()
    assert (len(user_transaction.objects) == 1)

    ts = repo.get_transactions_before_date(1,"2019-01-01")
    assert (len(ts) == 0)

    ts = repo.get_transactions_before_date(1,"2020-01-01")
    assert (len(ts) == 1)

    ts = repo.get_transactions_before_date(1,"2019-12-31")
    assert (len(ts) == 0)

    dt_now = datetime.today()

    ts = repo.get_transactions_before_date(1,dt_now)
    assert (len(ts) == 1)

