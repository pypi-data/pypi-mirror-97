from cryptomodel.cryptostore import user_notification, user_channel, user_settings
from cryptomodel.operations import OPERATIONS

from cryptodataaccess.Memory import Memory, USER_NOTIFICATIONS_MEMORY_KEY, USER_SETTINGS_MEMORY_KEY, \
    USER_CHANNELS_MEMORY_KEY
from cryptodataaccess.Repository import Repository

DATE_FORMAT = "%Y-%m-%d"


class UsersRepository(Repository):

    def __init__(self, users_store):
        super(UsersRepository, self).__init__()
        self.users_store = users_store
        self.notifications = []
        notification_memory = Memory(on_add=self.users_store.insert_notification,
                                     on_edit=self.users_store.update_notification,
                                     on_remove=self.users_store.delete_notification,
                                     items=self.notifications
                                     )
        self.memories[USER_NOTIFICATIONS_MEMORY_KEY] = notification_memory

        self.user_settings = []
        user_settings_memory = Memory(on_add=self.users_store.insert_user_settings,
                                      on_edit=self.users_store.update_user_settings,
                                      on_remove=self.users_store.delete_user_settings,
                                      items=self.user_settings
                                      )
        self.memories[USER_SETTINGS_MEMORY_KEY] = user_settings_memory

        self.user_channels = []
        user_channels_memory = Memory(on_add=self.users_store.insert_user_channel,
                                      on_edit=None,
                                      on_remove=None,
                                      items=self.user_channels
                                      )
        self.memories[USER_CHANNELS_MEMORY_KEY] = user_channels_memory

    def get_user_channels(self, user_id):
        return self.users_store.get_user_channels(user_id)

    def get_user_settings(self, user_id):
        return self.users_store.fetch_user_settings(user_id)

    def get_notification(self, notification_id):
        return self.users_store.fetch_notification_by_id(notification_id)

    def get_notifications(self):
        return self.users_store.fetch_notifications()

    def add_notification(self, user_id, user_name, user_email, notification_type, check_every,is_active,
                         start_date, end_date, channel_type, threshold_value, source_id):
        n = user_notification(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            notification_type=notification_type,
            check_every=check_every,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            channel_type=channel_type,
            threshold_value=threshold_value,
            source_id=source_id,
            operation=OPERATIONS.ADDED.name)
        self.memories[USER_NOTIFICATIONS_MEMORY_KEY].items.append(n)
        return n

    def edit_notification(self, in_id, user_id, user_name, user_email, notification_type, check_every,
                          start_date,end_date, is_active, channel_type, threshold_value, source_id):
        n = user_notification(id=in_id,
            user_id=user_id, user_name=user_name,
            user_email=user_email, notification_type=notification_type,
            check_every=check_every, start_date=start_date, end_date=end_date, is_active=is_active,
            channel_type=channel_type, threshold_value=threshold_value, source_id=source_id,
            operation=OPERATIONS.MODIFIED.name)
        self.memories[USER_NOTIFICATIONS_MEMORY_KEY].items.append(n)
        return n

    def add_user_settings(self, user_id, preferred_currency, source_id):
        uc = user_settings(user_id=user_id, preferred_currency=preferred_currency,
                           source_id=source_id, operation=OPERATIONS.ADDED.name)
        self.memories[USER_SETTINGS_MEMORY_KEY].items.append(uc)
        return uc

    def edit_user_settings(self, user_id, preferred_currency, source_id):
        uc = user_settings(user_id=user_id,
                           preferred_currency=preferred_currency,
                           source_id=source_id,
                           operation=OPERATIONS.MODIFIED.name)
        self.memories[USER_SETTINGS_MEMORY_KEY].items.append(uc)
        return uc

    def add_user_channel(self, user_id, channel_type, chat_id, source_id):
        uc = user_channel(
            user_id=user_id,
            channel_type=channel_type,
            chat_id=chat_id,
            operation=OPERATIONS.ADDED.name,
            source_id=source_id)
        self.memories[USER_CHANNELS_MEMORY_KEY].items.append(uc)
        return uc

    def remove_notification(self, in_id):
        self.mark_deleted(memory_key=USER_NOTIFICATIONS_MEMORY_KEY,
                          on_select=self.users_store.fetch_notification_by_id, id_value=in_id, id_name="id")

    def remove_user_setting(self, in_id):
        self.mark_deleted(memory_key=USER_CHANNELS_MEMORY_KEY,
                          on_select=self.users_store.fetch_user_settings_by_id, id_value=in_id, id_name="id")

    def remove_notification_by_source_id(self, source_id):
        self.mark_deleted(memory_key=USER_NOTIFICATIONS_MEMORY_KEY,
                          on_select=self.users_store.fetch_notification_by_id, id_value=source_id, id_name="source_id")
