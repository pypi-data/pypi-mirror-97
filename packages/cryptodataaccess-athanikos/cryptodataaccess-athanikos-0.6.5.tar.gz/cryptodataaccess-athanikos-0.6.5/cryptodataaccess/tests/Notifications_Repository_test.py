from datetime import datetime

import mock
from bson import ObjectId

from cryptomodel.operations import OPERATIONS
from cryptodataaccess.Memory import NOTIFICATIONS_MEMORY_KEY
from cryptodataaccess.config import configure_app
from cryptodataaccess.Notifications.NotificationsRepository import NotificationsRepository
from cryptodataaccess.Notifications.NotificationsMongoStore import NotificationsMongoStore
import pytest
from cryptodataaccess.helpers import do_local_connect
from cryptomodel.sent_notification import sent_notification

@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_insert_sent_notification():
    config = configure_app()
    store = NotificationsMongoStore(config, mock_log)
    repo = NotificationsRepository(store)
    do_local_connect(config)
    sent_notification.objects.all().delete()
    ut = repo.add_sent_notification(user_name="as",user_email="sa",user_id=1,threshold_value=1,notification_type="BALANCE",
                                    check_every="00:00",channel_type="TELEGRAM",is_active="False",
                                    start_date=datetime.now(),end_date=datetime.now(),
                                    source_id=ObjectId('666f6f2d6261722d71757578'), result="ds", computed_date=datetime.now)



    repo.commit()

    ut = repo.memories[NOTIFICATIONS_MEMORY_KEY].items[0]
    assert (ut.user_id == 1)
    assert (ut.operation == OPERATIONS.ADDED.name)
