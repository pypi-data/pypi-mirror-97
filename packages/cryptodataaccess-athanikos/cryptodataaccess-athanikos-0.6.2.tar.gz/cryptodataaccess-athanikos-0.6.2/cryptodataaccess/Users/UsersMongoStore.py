from abc import ABC

from cryptomodel.operations import OPERATIONS
from mongoengine import Q
from cryptomodel.cryptostore import user_notification, user_channel, user_transaction
from cryptomodel.cryptostore import user_settings
from cryptodataaccess.helpers import server_time_out_wrapper, if_none_raise, if_none_raise_with_id
from cryptodataaccess.Users.UsersStore import UsersStore
from cryptodataaccess.helpers import do_local_connect

DATE_FORMAT = "%Y-%m-%d"


class UsersMongoStore(UsersStore, ABC):

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_user_channels(self, user_id):
        return server_time_out_wrapper(self, self.do_fetch_user_channels, user_id)

    def fetch_user_settings(self, user_id):
        return server_time_out_wrapper(self, self.do_fetch_user_settings, user_id)

    def fetch_notifications(self, items_count):
        return server_time_out_wrapper(self, self.do_fetch_notifications, items_count)

    def fetch_notification_by_id(self, id):
        return server_time_out_wrapper(self, self.do_fetch_notification_by_id, id)

    def fetch_user_channel_by_id(self, id):
        return server_time_out_wrapper(self, self.do_fetch_user_channel_by_id, id)

    def insert_notification(self, notification):
        return server_time_out_wrapper(self, self.do_insert_notification, notification)

    def update_notification(self, notification):
        return server_time_out_wrapper(self, self.do_update_notification, notification)

    def fetch_user_settings_by_id(self, id):
        return server_time_out_wrapper(self, self.do_fetch_user_settings_by_id, id)

    def update_user_settings(self, user_settings):
        return server_time_out_wrapper(self, self.do_update_user_settings, user_settings)

    def insert_user_settings(self, user_settings):
        return server_time_out_wrapper(self, self.do_insert_user_settings, user_settings)

    def fetch_user_user_channel_by_id(self, id):
        return server_time_out_wrapper(self, self.do_fetch_user_channel_by_id, id)

    def insert_user_channel(self, user_channel):
        return server_time_out_wrapper(self, self.do_insert_user_channel, user_channel)

    def delete_notification(self, notification, throw_if_does_not_exist=True):
        server_time_out_wrapper(self, self.do_delete_notification, notification, throw_if_does_not_exist)

    def delete_user_settings(self, us):
        server_time_out_wrapper(self, self.do_delete_user_settings, us)

    def do_insert_notification(self, notification):
        do_local_connect(self.configuration)
        un = user_notification()
        un.user_id = notification.user_id
        un.user_name = notification.user_name
        un.user_email = notification.user_email
        un.notification_type = notification.notification_type
        un.check_every =notification.check_every
        un.start_date = notification.start_date
        un.end_date = notification.end_date
        un.is_active = notification.is_active
        un.channel_type = notification.channel_type
        un.threshold_value = notification.threshold_value
        un.source_id = notification.source_id
        un.operation = notification.operation
        un.save()
        return user_notification.objects(id=un.id).first()

    def do_insert_user_channel(self, in_uc):
        do_local_connect(self.configuration)
        uc = user_channel()
        uc.user_id = in_uc.user_id
        uc.channel_type = in_uc.channel_type
        uc.chat_id = in_uc.chat_id
        uc.operation = in_uc.operation
        uc.source_id = in_uc.source_id
        uc.save()
        return user_channel.objects(id=uc.id).first()

    def do_insert_user_settings(self, in_uc):
        do_local_connect(self.configuration)
        us = user_settings()
        us.user_id = in_uc.user_id
        us.preferred_currency = in_uc.preferred_currency
        us.operation = in_uc.operation
        us.source_id = in_uc.source_id
        us.save()
        return user_settings.objects(id=us.id).first()

    def do_update_user_settings(self, user_setting):
        do_local_connect(self.configuration)
        us = user_setting.objects(id=user_setting.id).first()
        if_none_raise_with_id(user_setting.id, us)
        us.user_id = user_setting.user_id
        us.preferred_currency = user_setting.preferred_currency
        us.save()
        return user_setting.objects(id=id).first()

    def do_update_notification(self, notification):
        do_local_connect(self.configuration)
        un = user_notification.objects(id=notification.id).first()
        if_none_raise_with_id(notification.id, un)
        un.user_id = notification.user_id
        un.user_name = notification.user_name
        un.user_email = notification.user_email
        un.notification_type = notification.notification_type

        un.check_every = notification.check_every
        un.start_date = notification.start_date
        un.end_date = notification.end_date

        un.is_active = notification.is_active
        un.channel_type = notification.channel_type
        un.threshold_value = notification.threshold_value
        un.source_id = notification.source_id
        un.operation = notification.operation
        un.save()
        return user_notification.objects(id=un.id).first()

    def delete_user_notification_by_source_id(self, source_id, throw_if_does_not_exist=True):
        server_time_out_wrapper(self, self.do_delete_user_notification_by_source_id, source_id,
                                throw_if_does_not_exist)

    def do_delete_user_notification_by_source_id(self, source_id, throw_if_does_not_exist=True):
        do_local_connect(self.configuration)
        un = user_notification.objects(source_id=source_id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(id, un)
        if un is not None:
            un.delete()

    def do_delete_notification(self, notif, throw_if_does_not_exist=True):
        do_local_connect(self.configuration)
        un = user_notification.objects(id=notif.id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(id, un)
        if un is not None:
            un.delete()

    def do_delete_user_settings(self, us):
        do_local_connect(self.configuration)
        us = user_settings.objects(id=us.id).first()
        if_none_raise_with_id(us.id, us)
        us.delete()

    def do_fetch_user_channels(self, user_id):
        do_local_connect(self.configuration)
        return user_notification.objects(Q(user_id=user_id))

    def do_fetch_user_settings(self, user_id):
        do_local_connect(self.configuration)
        return user_settings.objects(Q(user_id=user_id))

    def do_fetch_notifications(self, items_count):
        do_local_connect(self.configuration)
        return user_notification.objects()[:items_count]

    def do_fetch_user_channel_by_id(self, id):
        do_local_connect(self.configuration)
        return user_channel.objects(Q(id=id))

    def do_fetch_user_settings_by_id(self, id):
        do_local_connect(self.configuration)
        return user_settings.objects(Q(id=id))

    def do_fetch_notification_by_id(self, id):
        do_local_connect(self.configuration)
        return user_notification.objects(Q(id=id))
