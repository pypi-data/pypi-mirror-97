from mongoengine import Q
from cryptodataaccess.Transactions.TransactionStore import TransactionStore
from cryptodataaccess.helpers import if_none_raise_with_id
from cryptodataaccess import helpers
from cryptomodel.cryptostore import user_transaction


class TransactionMongoStore(TransactionStore):

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_distinct_user_ids(self):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transaction, id)

    def fetch_transaction(self, _id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transaction, _id)

    def fetch_transactions(self, user_id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transactions, user_id)

    def fetch_transactions_before_date(self, user_id, date):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transactions_before_date, user_id, date)

    def fetch_transactions(self, user_id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transactions, user_id)

    def fetch_distinct_user_ids(self):
        return helpers.server_time_out_wrapper(self, self.do_fetch_distinct_user_ids)

    def insert_transaction(self, in_trans):
        return helpers.server_time_out_wrapper(self, self.do_insert_transaction, in_trans)

    def update_transaction(self, in_trans):
        return helpers.server_time_out_wrapper(self, self.do_update_transaction, in_trans)

    def delete_transaction(self, in_trans, throw_if_not_exist):
        helpers.server_time_out_wrapper(self, self.do_delete_transaction, in_trans, throw_if_not_exist)

    def do_delete_transaction(self, in_trans, throw_if_does_not_exist=True):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(id=in_trans.id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(in_trans.id, trans)
        if trans is not None:
            trans.delete()

    def delete_transaction_by_source_id(self, source_id, throw_if_does_not_exist=True):
        helpers.server_time_out_wrapper(self, self.do_delete_transaction, source_id, throw_if_does_not_exist)

    def do_delete_transaction_by_source_id(self, source_id, throw_if_does_not_exist=True):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(source_id=source_id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(id, trans)
        if trans is not None:
            trans.delete()

    def do_update_transaction(self, in_trans):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(id=in_trans.id).first()
        if_none_raise_with_id(in_trans.id, trans)
        trans.user_id = in_trans.user_id
        trans.volume = in_trans.volume
        trans.symbol = in_trans.symbol
        trans.value = in_trans.value
        trans.price = in_trans.price
        trans.date = in_trans.date
        trans.currency = in_trans.currency
        trans.source = in_trans.source
        trans.source_id = in_trans.source_id
        trans.operation = in_trans.operation
        trans.type = in_trans.type
        trans.order_type = in_trans.order_type
        trans.save()
        return user_transaction.objects(id=trans.id).first()

    def do_insert_transaction(self, in_trans):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction()
        trans.user_id = in_trans.user_id
        trans.volume = in_trans.volume
        trans.symbol = in_trans.symbol
        trans.value = in_trans.value
        trans.price = in_trans.price
        trans.date = in_trans.date
        trans.currency = in_trans.currency
        trans.source = in_trans.source
        trans.source_id = in_trans.source_id
        trans.operation = in_trans.operation
        trans.is_valid = in_trans.is_valid
        trans.type = in_trans.type
        trans.order_type = in_trans.order_type
        trans.invalid_reason = in_trans.invalid_reason
        trans.save()
        return user_transaction.objects(id=trans.id).first()

    def do_fetch_transactions(self, user_id):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects(Q(user_id=user_id))

    def do_fetch_transactions_before_date(self, user_id, date):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects(Q(user_id=user_id) &
                                        Q(date__lte=date)
                                        )

    def do_fetch_transaction(self, id):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(Q(id=id))
        if len(trans) == 1:
            return user_transaction.objects(Q(id=id))[0]
        return None

    def do_fetch_distinct_user_ids(self):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects().only('user_id').distinct('user_id')
