from abc import ABCMeta, abstractmethod


class TransactionStore(metaclass=ABCMeta):
    @abstractmethod
    def fetch_distinct_user_ids(self):
        pass

    @abstractmethod
    def fetch_distinct_user_ids(self):
        pass

    @abstractmethod
    def fetch_transaction(self, id):
        pass

    @abstractmethod
    def fetch_transactions(self, user_id):
        pass

    @abstractmethod
    def fetch_transactions(self, user_id):
        pass

    @abstractmethod
    def fetch_transactions_before_date(self, user_id, date):
        pass

    @abstractmethod
    def insert_transaction(self, user_id, volume, symbol, value, price, currency, date, source, source_id, operation):
        pass

    @abstractmethod
    def update_transaction(self, id, user_id, volume, symbol, value, price, currency, date, source, source_id,
                           operation):
        pass

    @abstractmethod
    def delete_transaction(self, id, throw_if_does_not_exist):
        pass

    @abstractmethod
    def delete_transaction_by_source_id(self, source_id, throw_if_does_not_exist):
        pass
