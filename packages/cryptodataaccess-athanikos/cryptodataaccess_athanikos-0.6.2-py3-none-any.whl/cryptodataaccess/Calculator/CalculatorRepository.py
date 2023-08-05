from cryptomodel.computed_notification import computed_notification
from cryptomodel.operations import OPERATIONS

from cryptodataaccess.Memory import Memory, CALCULATOR_MEMORY_KEY
from cryptodataaccess.Repository import Repository

DATE_FORMAT = "%Y-%m-%d"


class CalculatorRepository(Repository):

    def __init__(self, calculator_store):
        self.calculator_store = calculator_store
        self.computed_notifications = []
        super(CalculatorRepository, self).__init__()
        memory = Memory(on_add=self.calculator_store.insert_computed_notification,
                        on_edit=None,
                        on_remove=None,
                        items=self.computed_notifications
                        )
        self.memories[CALCULATOR_MEMORY_KEY] = memory

    def add_computed_notification(self, user_id, user_name, user_email, notification_type, check_every, is_active,
                                  start_date, end_date, channel_type, threshold_value, source_id, computed_date, result,
                                  ):
        n = computed_notification(
            user_id=user_id, user_name=user_name, user_email=user_email,
            notification_type=notification_type,
            check_every=check_every,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            channel_type=channel_type, threshold_value=threshold_value, source_id=source_id,
            operation=OPERATIONS.ADDED.name, computed_date=computed_date, result=result)

        self.memories[CALCULATOR_MEMORY_KEY].items.append(n)
        return n

    def edit_computed_notification(self, user_id, user_name, user_email, notification_type, check_every, is_active,
                                  start_date, end_date, channel_type, threshold_value, source_id, computed_date, result):
        n = computed_notification(
            user_id=user_id, user_name=user_name, user_email=user_email,
            notification_type=notification_type,
            check_every=check_every,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            channel_type=channel_type, threshold_value=threshold_value, source_id=source_id,
            operation=OPERATIONS.MODIFIED.name, computed_date=computed_date, result=result)

        self.memories[CALCULATOR_MEMORY_KEY].items.append(n)
        return n

    def get_computed_notification_before_date(self, user_id, date):
        return self.calculator_store.fetch_computed_notifications_before_date(user_id, date)

