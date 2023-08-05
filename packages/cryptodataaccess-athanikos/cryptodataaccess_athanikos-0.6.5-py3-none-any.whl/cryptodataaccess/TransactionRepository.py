from cryptomodel.cryptostore import user_notification, user_channel, user_transaction, operation_type
from mongoengine import Q
from cryptodataaccess import helpers
from cryptodataaccess.helpers import if_none_raise, if_none_raise_with_id


class TransactionRepository:

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_distinct_user_ids(self):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transaction, id)

    def fetch_transaction(self, id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transaction, id)

    def fetch_transactions(self, user_id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transactions, user_id)

    def fetch_transactions(self, user_id):
        return helpers.server_time_out_wrapper(self, self.do_fetch_transactions, user_id)

    def fetch_distinct_user_ids(self):
        return helpers.server_time_out_wrapper(self, self.do_fetch_distinct_user_ids())

    def insert_transaction(self, user_id, volume, symbol, value, price, currency, date, source, source_id, operation):
        return helpers.server_time_out_wrapper(self, self.do_insert_transaction, user_id, volume, symbol,
                                               value, price, currency, date, source, source_id, operation)

    def update_transaction(self, id, user_id, volume, symbol, value, price, currency, date, source, source_id,
                           operation):
        return helpers.server_time_out_wrapper(self, self.do_update_transaction, id,
                                               user_id, volume, symbol, value, price, currency, date, source, source_id,
                                               operation)

    def delete_transaction(self, id, throw_if_does_not_exist=True):
        helpers.server_time_out_wrapper(self, self.do_delete_transaction, id, throw_if_does_not_exist)

    def do_delete_transaction(self, id, throw_if_does_not_exist=True):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(id=id).first()
        if throw_if_does_not_exist:
            if_none_raise_with_id(id, trans)
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

    def do_update_transaction(self, id, user_id, volume, symbol, value, price, currency, date, source, source_id,
                              operation):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction.objects(id=id).first()
        if_none_raise_with_id(id, trans)
        trans.user_id = user_id
        trans.volume = volume
        trans.symbol = symbol
        trans.value = value
        trans.price = price
        trans.date = date
        trans.source = source
        trans.currency = currency
        trans.source_id = source_id
        trans.operation = operation
        trans.save()
        return user_transaction.objects(id=id).first()

    def do_insert_transaction(self, user_id, volume, symbol, value, price, currency, date, source, source_id,
                              operation):
        helpers.do_local_connect(self.configuration)
        trans = user_transaction()
        trans.user_id = user_id
        trans.volume = volume
        trans.symbol = symbol
        trans.value = value
        trans.price = price
        trans.date = date
        trans.currency = currency
        trans.source = source
        trans.source_id = source_id
        trans.operation = operation
        trans.save()
        return user_transaction.objects(id=trans.id).first()

    def do_fetch_transactions(self, user_id ):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects(Q(user_id=user_id))

    def do_fetch_transaction(self,id):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects(Q(id=id))[0]

    def do_fetch_distinct_user_ids(self):
        helpers.do_local_connect(self.configuration)
        return user_transaction.objects().only('user_id').distinct('user_id')
