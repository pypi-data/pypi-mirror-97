from abc import ABCMeta, abstractmethod


class UsersStore(metaclass=ABCMeta):

    @abstractmethod
    def fetch_user_channels(self, user_id):
        pass

    @abstractmethod
    def fetch_notifications(self):
        pass

    @abstractmethod
    def fetch_notification_by_id(self, id):
        pass

    @abstractmethod
    def insert_notification(self, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                            check_times, is_active, channel_type, fields_to_send, source_id, operation):
        pass

    @abstractmethod
    def update_notification(self, id, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                            check_times, is_active, channel_type, fields_to_send, source_id, operation):
        pass


    @abstractmethod
    def fetch_user_settings_by_id(self, id):
        pass

    @abstractmethod
    def update_user_settings(self, user_id, preferred_currency):
        pass

    @abstractmethod
    def insert_user_settings(self, user_id, preferred_currency):
        pass

    @abstractmethod
    def fetch_user_channel_by_id(self, id):
        pass

    @abstractmethod
    def insert_user_channel(self, user_id, channel_type, chat_id):
        pass

    @abstractmethod
    def delete_notification(self, id):
        pass

    @abstractmethod
    def delete_user_settings(self, id):
        pass
