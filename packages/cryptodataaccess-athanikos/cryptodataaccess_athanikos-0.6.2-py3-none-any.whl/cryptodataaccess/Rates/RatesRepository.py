from cryptodataaccess.Repository import Repository

DATE_FORMAT = "%Y-%m-%d"


class RatesRepository(Repository):

    def __init__(self, rates_store):
        self.rates_store = rates_store
        super(RatesRepository, self).__init__()

    def fetch_symbols(self):
        return self.rates_store.fetch_symbols()

    def fetch_symbol_rates(self):
        return self.rates_store.fetch_symbol_rates()

    def fetch_symbol_rates_for_date(self, dt):
        return self.rates_store.fetch_symbol_rates_for_date(dt)

    def fetch_latest_prices_to_date(self, before_date):
        return self.rates_store.fetch_latest_prices_to_date(before_date)

    def fetch_latest_exchange_rates_to_date(self, before_date):
        return self.rates_store.fetch_latest_exchange_rates_to_date(before_date)

    def insert_prices(self, status, data):
        return self.rates_store.insert_prices(status, data)

    def delete_prices(self, source_id ):
        return self.rates_store.delete_prices(source_id)

    def fetch_prices(self, source_id):
        return self.rates_store.fetch_prices(source_id)

