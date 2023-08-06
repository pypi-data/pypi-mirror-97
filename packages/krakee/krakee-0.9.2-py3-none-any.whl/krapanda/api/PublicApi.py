from pandas import DataFrame


class PublicApi:

    def __init__(self, kapi):
        self.kapi = kapi

    def assets(self) -> DataFrame:
        df = self.kapi.query_public("Assets")
        return DataFrame(df['result'])

    def assetPairs(self) -> DataFrame:
        df = self.kapi.query_public("AssetPairs")
        return DataFrame(df['result'])

    def ticker(self, *pairs) -> DataFrame:
        df = self.kapi.query_public("Ticker", data="pair=" + ",".join(pairs))
        return DataFrame(df['result'])

    def ohlc(self, pair, interval: str, since=None) -> DataFrame:
        valid_intervals = {"1min":1, "5min":5, "15min":15, "30min": 30, "1h":60, "4h":240, "1d":1440, "7d":10080, "15d":21600}
        assert (interval in valid_intervals)
        data = "pair={}&interval={}".format(pair, valid_intervals[interval])
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("OHLC", data=data)
        rows = response['result'][pair]
        ohlcdata = DataFrame.from_records(rows, columns=['time', 'o', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        last = response['result']['last']
        return ohlcdata, last

    def orderBook(self, pair, count=None) -> DataFrame:
        data = "pair={}".format(pair)
        if count:
            data = "{}&count={}".format(data, count)
        response = self.kapi.query_public("Depth", data)
        asks = response['result'][pair]['asks']
        bids = response['result'][pair]['bids']
        asksDf = DataFrame.from_records(asks, columns=['price', 'volume', 'timestamp'])
        bidsDf = DataFrame.from_records(bids, columns=['price', 'volume', 'timestamp'])
        asksDf['type'] = 'asks'
        bidsDf['type'] = 'bids'
        return asksDf.append(bidsDf, ignore_index=True)

    def trades(self, pair, since=None) -> DataFrame:
        data = "pair={}".format(pair)
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("Trades", data)
        last = response['result']['last']
        return DataFrame.from_records(
            response['result'][pair], columns=['price', 'volume', 'time', 'direction', 'type', 'misc']), last

    def spread(self, pair, since=None) -> DataFrame:
        data = "pair={}".format(pair)
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("Spread", data)
        last = response['result']['last']
        return DataFrame.from_records(response['result'][pair], columns=['time', 'bid', 'ask']), last
