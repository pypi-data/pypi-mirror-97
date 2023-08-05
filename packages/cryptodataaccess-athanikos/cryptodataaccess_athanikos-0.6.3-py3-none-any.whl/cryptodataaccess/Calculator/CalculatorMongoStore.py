from cryptodataaccess import helpers
from cryptodataaccess.Calculator.CalculatorStore import CalculatorStore
from cryptomodel.computed_notification import computed_notification, Q

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class CalculatorMongoStore(CalculatorStore):

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_computed_notification_before_date(self, user_id, date):
        return self.transaction_store.do_fetch_computed_notification_before_date(user_id, date)

    def insert_computed_notification(self, comp_not):
        return helpers.server_time_out_wrapper(self, self.do_insert_computed_notification, comp_not)

    def do_insert_computed_notification(self, _computed_notification):
        helpers.do_local_connect(self.configuration)
        cn = computed_notification()
        cn.computed_date = _computed_notification.computed_date
        cn.result = _computed_notification.result
        cn.user_id = _computed_notification.user_id
        cn.user_name = _computed_notification.user_name
        cn.user_email = _computed_notification.user_email
        cn.notification_type = _computed_notification.notification_type

        cn.check_every = _computed_notification.check_every
        cn.start_date = _computed_notification.start_date
        cn.end_date = _computed_notification.end_date

        cn.is_active = _computed_notification.is_active
        cn.channel_type = _computed_notification.channel_type
        cn.threshold_value = _computed_notification.threshold_value
        cn.source_id = _computed_notification.source_id
        cn.operation = _computed_notification.operation
        cn.save()
        return computed_notification.objects(id=cn.id).first()

    def do_fetch_computed_notification_before_date(self, user_id, date):
        helpers.do_local_connect(self.configuration)
        return computed_notification.objects(Q(user_id=user_id) &
                                             Q(computed_date__lte=date)
                                             )
