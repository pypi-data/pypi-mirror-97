import logging
import logging as logger
from functools import wraps

import krakenex
import pandas
from pandas import DataFrame
from pykrakenapi import KrakenAPI

from krakee import OrderBuilder
from krakee.api import utils


# @cache decorator to cache responses
def cached(*args, **kwargs):
    func = None
    if len(args) == 1 :
        func = args[0]
    if func:
        always = False
    if not func:
        always = kwargs.get('always')

    def callable (func):

        @wraps (func)
        def wrapper(self, *args, **kwargs):
            func_name = func.__name__
            cachedValue = None
            str_args = "_".join(list(map(lambda x: str(x), args)))
            cachedId = "_".join([func_name, str_args])
            if self.is_cached or always:
                if cachedId in self.cache:
                    cachedValue = self.cache[cachedId]
                    logger.info ("Cache::retrieving {}({}) from cache...".format(func_name, cachedId))
            if cachedValue is None:
                cachedValue = func(self, *args, **kwargs)
                if self.cache or always:
                    self.cache[cachedId] = cachedValue
            return cachedValue
        return wrapper
    return callable(func) if func else callable


class Krakee:

    """Initiates a new Krakee instance

        Creates a new Krakee instance. On start, the list of asset pairs is always fetched and cached, as it's
        unlikely that it will change during the object lifecycle and it's used to validate method parameters.

        Attributes
        ----------
        authfile: path to the file with two lines, containing auth token and private key, in that order.
        full_caching: if True, all requests to Kraken Public API will be run and then cached. Any onward invocation
                      will see the cached content. Disabled by default.
        """
    def __init__(self, authfile=None, full_caching=False):
        logging.basicConfig(level=logging.INFO)
        self.cache = {}
        self.is_cached = full_caching
        if authfile:
            with open(authfile, 'r') as f:
                public_key = f.readline().strip()
                secret_key = f.readline().strip()
                self.kapi = KrakenAPI(krakenex.API(public_key, secret_key), crl_sleep=2)
                logger.info("Auth keys successfully loaded from {}".format(authfile))
        else:
            self.kapi = KrakenAPI(krakenex.API(), crl_sleep=2)
            logger.info("Auth token not provided, only public API available")
        self.asset_pairs()

    @cached(always=True)
    def assets(self) -> DataFrame: return self.kapi.get_asset_info().transpose()

    @cached (always=True)
    def asset_pairs(self) -> DataFrame: return self.kapi.get_tradable_asset_pairs().transpose()

    @cached
    def tickers(self, pairs) -> DataFrame:
        utils.assert_list(pairs, "pairs")
        utils.asset_pair(self, pairs)
        assetList = [pairs[n:n + 9] for n in range(0, len(pairs), 9)]
        logger.info ("Tickers::requesting {} set of tickers, it will take aprox. {}s".format(len(assetList), (len(assetList)-1)*5))
        tickers = [self.kapi.get_ticker_information(",".join(assets)) for assets in assetList]
        tickerDf = pandas.concat(tickers)
        tickerDf = utils.dataframe_to_numeric(tickerDf).transpose()
        logger.info ("Tickers::retrieved {} tickers".format(len(tickerDf.columns)))
        return tickerDf

    """Returns OHLC data for given pairs
    
    Returns the OHLC data for given pairs as a map pair->OHLC data. 
    This may take a while if several asset pairs are provided.
    
    Attributes
    ----------
    pairs: list of asset pairs
    interval: one of allowed interval values
    since: optional since timestamp
    """
    @cached
    def ohlc(self, pairs, interval: str = "1min", since=None) -> map:
        utils.assert_list(pairs, "pairs")
        utils.asset_pair (self, pairs)
        intervals = {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "1h": 60, "4h": 240, "1d": 1440, "7d": 10080, "15d": 21600}
        utils.assert_interval(interval, intervals)
        ohlcList = {pair:self.kapi.get_ohlc_data(pair, intervals[interval], since) for pair in pairs}
        return ohlcList

    @cached
    def order_book(self, pair, count=None) -> (DataFrame, DataFrame):
        utils.asset_pair(self, pair)
        return self.kapi.get_order_book(pair, count)

    @cached
    def trades(self, pair, since=None) -> DataFrame:
        utils.asset_pair(self, pair)
        return self.kapi.get_recent_trades (pair, since)

    @cached
    def spread(self, pair, since=None) -> DataFrame:
        utils.asset_pair(self, pair)
        return self.kapi.get_recent_spread_data (pair, since)

    # Private API

    @cached
    def add_order (self, order_builder: OrderBuilder):
        return self.kapi.api.query_private("AddTrade", order_builder.build())

    @cached
    def balance(self): return self.kapi.get_account_balance()

    @cached
    def trade_balance (self): return self.kapi.get_trade_balance()

    @cached
    def open_orders (self): return self.kapi.get_open_orders()

    @cached
    def closed_orders (self): return self.kapi.get_closed_orders()

    # Extras

    """Returns asset pairs with given quote currency. E.g. XXBTUSD quote is 'USD'
    
    From the whole set of asset pairs, filters the ones with given quote currency.
    
    Parameters
    ----------
    currency: the currency to look for
 
    """
    def asset_pairs_by_quote_currency (self, currency):
        ap =  self.asset_pairs()
        currencies = set(ap.loc['quote'])
        assert (currency in currencies), "currency must be one of {}".format(currencies)
        return ap.loc[:, ap.loc['quote'] == currency]

    """Returns the list of currencies defined in all the asset pairs
    """
    def currencies (self):
        return list(set(self.asset_pairs().loc['quote']))