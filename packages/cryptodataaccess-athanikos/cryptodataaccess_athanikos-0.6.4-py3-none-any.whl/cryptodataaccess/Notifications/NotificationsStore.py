from abc import ABCMeta, abstractmethod


class NotificationsStore(metaclass=ABCMeta):

    @abstractmethod
    def fetch_unsent_notifications(self, user_id, user_name, user_email, notification_type, check_every, is_active,
                              start_date, end_date, channel_type, threshold_value, source_id, computed_date, result,
                              sent=False):
        pass

    @abstractmethod
    def insert_sent_notification(self):
        pass



