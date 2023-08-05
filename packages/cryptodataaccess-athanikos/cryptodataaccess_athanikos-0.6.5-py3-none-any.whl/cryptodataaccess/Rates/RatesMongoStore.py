from datetime import datetime
from cryptomodel.fixer import exchange_rates, Q
from cryptomodel.readonly import SymbolRates
from cryptomodel.coinmarket import prices
from cryptodataaccess.Rates.RatesStore import RatesStore
from cryptodataaccess.helpers import server_time_out_wrapper, do_local_connect, convert_to_int_timestamp
from cryptodataaccess.helpers import  do_central_connect
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


''' 
Provides a set of methods of CRUD opearations for prices and exchange rates 
'''

class RatesMongoStore(RatesStore):

    def __init__(self, config, log_error, is_local_connect=True):
        self.configuration = config
        self.log_error = log_error
        self.is_local_connect = is_local_connect

    def fetch_symbols(self):
        symbols = {}
        latest_prices = self.fetch_latest_prices_to_date( convert_to_int_timestamp(datetime.today()))
        for coin in latest_prices[0].coins:
            symbols.update({coin.symbol: coin.name})
        return symbols

    def fetch_symbol_rates(self):
        dt_now = convert_to_int_timestamp(datetime.today())
        return self.fetch_symbol_rates_for_date(dt_now)

    def fetch_symbol_rates_for_date(self, dt):
        srs = SymbolRates(dt)
        latest_prices = self.fetch_latest_prices_to_date(dt)
        for coin in latest_prices[0].coins:
            srs.add_rate(coin.symbol, coin.quote.eur)
        return srs

    def fetch_latest_prices_to_date(self, before_date):
        return server_time_out_wrapper(self, self.do_fetch_latest_prices_to_date, before_date)

    def fetch_latest_exchange_rates_to_date(self, before_date):
        return server_time_out_wrapper(self, self.do_fetch_latest_exchange_rates_to_date, before_date)

    def do_fetch_latest_prices_to_date(self, before_date):
        if self.is_local_connect:
            do_local_connect(self.configuration)
        else:
            do_central_connect(self.configuration)

        return prices.objects(Q(status__timestamp__lte=before_date)).order_by(
            '-status__timestamp')[:10]

    def do_fetch_latest_exchange_rates_to_date(self, before_date):
        if self.is_local_connect:
            do_local_connect(self.configuration)
        else:
            do_central_connect(self.configuration)

        return exchange_rates.objects(Q(date__lte=before_date)).order_by(
            'date-')[:1]

    def delete_prices(self,  source_id):
        if self.is_local_connect:
            do_local_connect(self.configuration)
        else:
            do_central_connect(self.configuration)

        price = prices.objects(Q(source_id=source_id)).first()
        if price is not None:
            price.delete()

    def do_delete_symbols(self, source_id):
        return server_time_out_wrapper(self, self.do_delete_symbols,  source_id)

    def insert_prices(self, prc ):
        return server_time_out_wrapper(self, self.do_insert_prices, prc)

    def do_insert_prices(self, prc ):
        if self.is_local_connect:
            do_local_connect(self.configuration)
        else:
            do_central_connect(self.configuration)

        prcs = prices()
        prcs.status = prc.status
        prcs.coins = prc.coins
        prcs.source_id = prc.source_id
        prcs.save()

    def fetch_prices(self, source_id):
        return server_time_out_wrapper(self, self.do_fetch_prices, source_id)

    def do_fetch_prices(self, source_id):
        if self.is_local_connect:
            do_local_connect(self.configuration)
        else:
            do_central_connect(self.configuration)
        return prices.objects(Q(source_id=source_id))

