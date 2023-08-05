from mongoengine import Q
from cryptomodel.cryptostore import user_notification, user_channel, user_transaction, operation_type
from cryptomodel.cryptostore import user_settings
from cryptodataaccess import helpers
from cryptodataaccess.helpers import if_none_raise, if_none_raise_with_id

DATE_FORMAT = "%Y-%m-%d"


class UsersRepository:

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_user_channels(self, user_id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_user_channels, user_id)

    def fetch_notifications(self, items_count):
        return helpers.server_time_out_wrapper(self, self.do_fetch_notifications, items_count)

    def insert_notification(self, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                            check_times, is_active, channel_type, fields_to_send,source_id, operation):
        return helpers.server_time_out_wrapper(self, self.do_insert_notification, user_id, user_name, user_email,
                                               expression_to_evaluate, check_every_seconds,
                                               check_times, is_active, channel_type, fields_to_send,source_id, operation)

    def update_notification(self,id, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                            check_times, is_active, channel_type, fields_to_send,source_id, operation):
        return helpers.server_time_out_wrapper(self, self.do_update_notification, id, user_id, user_name, user_email,
                                               expression_to_evaluate, check_every_seconds,
                                               check_times, is_active, channel_type, fields_to_send,source_id, operation)

    def update_user_settings(self, user_id, preferred_currency):
        return helpers.server_time_out_wrapper(self, self.do_update_user_settings, user_id, preferred_currency)

    def insert_user_settings(self, user_id, preferred_currency):
        return helpers.server_time_out_wrapper(self, self.do_insert_user_channel, user_id, preferred_currency)

    def insert_user_channel(self, user_id, channel_type, chat_id):
        return helpers.server_time_out_wrapper(self, self.do_insert_user_channel, user_id, channel_type, chat_id)

    def delete_notification(self, id):
        helpers.server_time_out_wrapper(self, self.do_delete_notification, id)

    def delete_user_settings(self, id):
        helpers.server_time_out_wrapper(self, self.do_delete_user_settings, id)

    def do_fetch_user_channels(self, user_id):
        helpers.do_local_connect(self.configuration)
        return user_notification.objects(Q(user_id=user_id))

    def do_fetch_notifications(self, items_count):
        helpers.do_local_connect(self.configuration)
        return user_notification.objects()[:items_count]

    def do_fetch_transactions(self, user_id):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects(Q(user_id=user_id))

    def do_insert_notification(self, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                               check_times, is_active, channel_type, fields_to_send,source_id, operation):
        helpers.do_local_connect(self.configuration)
        un = user_notification()
        un.user_id = user_id
        un.user_name = user_name
        un.user_email = user_email
        un.is_active = True
        un.expression_to_evaluate = expression_to_evaluate
        un.check_every_seconds = check_every_seconds
        un.check_times = check_times
        un.is_active = is_active
        un.channel_type = channel_type
        un.fields_to_send = fields_to_send
        un.source_id = source_id
        un.operation = operation
        un.save()
        return user_notification.objects(id=un.id).first()

    def do_insert_user_channel(self, user_id, channel_type, chat_id):
        helpers.do_local_connect(self.configuration)
        uc = user_channel()
        uc.userId = user_id
        uc.channel_type = channel_type
        uc.chat_id = chat_id
        uc.save()
        return user_channel.objects(id=uc.id).first()

    def do_insert_user_settings(self, user_id, preferred_currency):
        helpers.do_local_connect(self.configuration)
        us = user_settings()
        us.userId = user_id
        us.preferred_currency = preferred_currency
        us.save()
        return user_settings.objects(id=us.id).first()

    def do_update_user_settings(self, id, user_id, preferred_currency):
        helpers.do_local_connect(self.configuration)
        us = user_settings.objects(id=id).first()
        if_none_raise_with_id(id, us)
        us.user_id = user_id
        us.preferred_currency = preferred_currency
        us.save()
        return user_settings.objects(id=id).first()

    def do_update_notification(self, id, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                               check_times, is_active, channel_type, fields_to_send, source_id, operation):
        helpers.do_local_connect(self.configuration)
        un = user_notification.objects(id=id).first()
        if_none_raise_with_id(id, un)
        un.id = id
        un.userId = user_id
        un.user_name = user_name
        un.user_email = user_email
        un.is_active = True
        un.expression_to_evaluate = expression_to_evaluate
        un.check_every_seconds = check_every_seconds
        un.check_times = check_times
        un.is_active = is_active
        un.channel_type = channel_type
        un.fields_to_send = fields_to_send
        un.source_id = source_id
        un.operation = operation
        un.save()
        return user_notification.objects(id=un.id).first()

    def do_delete_notification(self, id):
        helpers.do_local_connect(self.configuration)
        un = user_notification.objects(id=id).first()
        if_none_raise_with_id(id, un)
        un.delete()

    def do_delete_user_settings(self, id):
        helpers.do_local_connect(self.configuration)
        us = user_settings.objects(id=id).first()
        if_none_raise_with_id(id, us)
        us.delete()

    def delete_user_notification_by_source_id(self, source_id, throw_if_does_not_exist=True):
        helpers.server_time_out_wrapper(self, self.do_delete_user_notification_by_source_id, source_id, throw_if_does_not_exist)

    def do_delete_user_notification_by_source_id(self, source_id, throw_if_does_not_exist=True):
        helpers.do_local_connect(self.configuration)
        un = user_notification.objects(source_id=source_id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(id, un)
        if un is not None:
            un.delete()