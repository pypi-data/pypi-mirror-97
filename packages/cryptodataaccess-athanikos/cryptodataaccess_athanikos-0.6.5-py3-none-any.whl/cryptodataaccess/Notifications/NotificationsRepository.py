from cryptomodel.operations import OPERATIONS
from cryptodataaccess.Memory import Memory, NOTIFICATIONS_MEMORY_KEY
from cryptodataaccess.Repository import Repository
from cryptomodel.sent_notification import sent_notification

DATE_FORMAT = "%Y-%m-%d"


class NotificationsRepository(Repository):

    def __init__(self, notifications_store):
        self.notifications_store = notifications_store
        self.sent_notifications = []
        super(NotificationsRepository, self).__init__()

        memory = Memory(on_add=self.notifications_store.insert_sent_notification,
                        on_edit=None,
                        on_remove=None,
                        items=self.sent_notifications
                        )
        self.memories[NOTIFICATIONS_MEMORY_KEY] = memory

    def add_sent_notification(self, user_id, user_name, user_email, notification_type, check_every, is_active,
                              start_date, end_date, channel_type, threshold_value, source_id, computed_date, result):
        n = sent_notification(
            user_id=user_id, user_name=user_name, user_email=user_email,
            notification_type=notification_type,
            check_every=check_every,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            channel_type=channel_type, threshold_value=threshold_value, source_id=source_id,
            operation=OPERATIONS.ADDED.name, computed_date=computed_date, result=result)

        self.memories[NOTIFICATIONS_MEMORY_KEY].items.append(n)
        return n

    def get_notification(self, id):
        return self.notifications_store.fetch_notification()
