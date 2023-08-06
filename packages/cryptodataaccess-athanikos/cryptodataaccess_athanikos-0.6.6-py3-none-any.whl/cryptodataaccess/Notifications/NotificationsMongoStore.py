
from cryptodataaccess import helpers
from cryptodataaccess.Notifications.NotificationsStore import NotificationsStore
from cryptomodel.sent_notification import sent_notification

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class NotificationsMongoStore(NotificationsStore):

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_unsent_notifications(self):
        raise NotImplementedError()

    def insert_sent_notification(self, comp_not):
        return helpers.server_time_out_wrapper(self, self.do_insert_sent_notification, comp_not)

    def do_insert_sent_notification(self, _sent_notification):
        helpers.do_local_connect(self.configuration)
        sn = sent_notification()
        sn.computed_date = _sent_notification.computed_date
        sn.result = _sent_notification.result
        sn.user_id = _sent_notification.user_id
        sn.user_name = _sent_notification.user_name
        sn.user_email = _sent_notification.user_email
        sn.notification_type = _sent_notification.notification_type

        sn.check_every = _sent_notification.check_every
        sn.start_date = _sent_notification.start_date
        sn.end_date = _sent_notification.end_date
        sn.check_every = _sent_notification.check_every
        sn.is_active = _sent_notification.is_active
        sn.channel_type = _sent_notification.channel_type
        sn.threshold_value = _sent_notification.threshold_value
        sn.source_id = _sent_notification.source_id
        sn.operation = _sent_notification.operation
        sn.computed_date = _sent_notification.computed_date
        sn.result = _sent_notification.result
        sn.save()
        return sent_notification.objects(id=sn.id).first()
