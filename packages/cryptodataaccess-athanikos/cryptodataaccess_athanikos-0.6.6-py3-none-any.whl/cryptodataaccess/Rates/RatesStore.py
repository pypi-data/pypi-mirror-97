from abc import ABCMeta, abstractmethod


class RatesStore(metaclass=ABCMeta):
    @abstractmethod
    def fetch_symbols(self):
        pass

    @abstractmethod
    def fetch_symbol_rates_for_date(self, dt):
        pass

    @abstractmethod
    def fetch_symbol_rates(self):
        pass

    @abstractmethod
    def fetch_latest_prices_to_date(self, before_date):
        pass

    @abstractmethod
    def fetch_latest_exchange_rates_to_date(self, before_date):
        pass

    @abstractmethod
    def insert_prices(self, id, status, coins , source_id):
        pass

    @abstractmethod
    def delete_prices(self, source_id):
        pass


    @abstractmethod
    def fetch_prices(self, source_id):
        pass

