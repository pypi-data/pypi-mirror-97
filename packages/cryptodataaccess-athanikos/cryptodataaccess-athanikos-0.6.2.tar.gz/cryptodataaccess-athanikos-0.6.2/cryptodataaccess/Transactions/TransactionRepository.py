from cryptomodel.cryptostore import user_transaction
from cryptomodel.operations import OPERATIONS

from cryptodataaccess.Memory import Memory, TRANSACTIONS_MEMORY_KEY
from cryptodataaccess.Repository import Repository


class TransactionRepository(Repository):

    def __init__(self, transaction_store):
        self.transaction_store = transaction_store
        self.transactions = []
        super(TransactionRepository, self).__init__()
        memory = Memory(on_add=self.transaction_store.insert_transaction,
                        on_edit=self.transaction_store.update_transaction,
                        on_remove=self.transaction_store.delete_transaction,
                        items=self.transactions
                        )
        self.memories[TRANSACTIONS_MEMORY_KEY] = memory

    def get_distinct_user_ids(self):
        return self.transaction_store.fetch_distinct_user_ids()

    def get_transaction(self, id):
        return self.transaction_store.fetch_transaction(id)

    def get_transactions(self, user_id):
        return self.transaction_store.fetch_transactions(user_id)

    def get_transactions_before_date(self, user_id, date):
        return self.transaction_store.fetch_transactions_before_date(user_id, date)

    def add_transaction(self, user_id, volume, symbol, value, price, currency, date, source, source_id, transaction_type,
                        order_type):
        t = user_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                             currency=currency, date=date, source=source, source_id=source_id,
                             operation=OPERATIONS.ADDED.name, is_valid=True, invalid_reason="",
                             type=transaction_type, order_type = order_type
                             )
        self.memories[TRANSACTIONS_MEMORY_KEY].items.append(t)
        return t

    def edit_transaction(self, in_id, user_id, volume, symbol, value, price, currency, date, source, source_id, transaction_type,
                         order_type):
        t = user_transaction(id=in_id,
                             user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                             currency=currency, date=date, source=source, source_id=source_id,
                             operation=OPERATIONS.MODIFIED.name,
                             type=transaction_type, order_type=order_type
                             )
        self.memories[TRANSACTIONS_MEMORY_KEY].items.append(t)
        return t

    def remove_transaction(self, in_id):
        self.mark_deleted(memory_key=TRANSACTIONS_MEMORY_KEY,
                          on_select=self.transaction_store.fetch_transaction, id_value=in_id, id_name="id")

    def remove_transaction_by_source_id(self, source_id):
        self.mark_deleted(memory_key=TRANSACTIONS_MEMORY_KEY,
                          on_select=self.transaction_store.fetch_transaction, id_value=source_id, id_name="source_id")
