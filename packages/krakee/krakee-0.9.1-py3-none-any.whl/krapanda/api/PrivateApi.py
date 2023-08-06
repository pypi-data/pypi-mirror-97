from urllib.error import HTTPError

import krakenex
from pandas import DataFrame


class PrivateApi:

    def __init__(self, kapi):
        self.kapi = kapi

    def balance(self) -> DataFrame:
        response = self.kapi.query_private("Balance")
        return DataFrame(response['result'], index=[0], dtype=float)

    def openOrders(self):
        response = self.kapi.query_private("OpenOrders")

    def closedOrders(self, start, end) -> DataFrame:
        data = {'start': start, 'end': end}
        response = self.kapi.query_private("ClosedOrders", data)
        closedOrders = response['result']['closed']
        df = DataFrame.from_dict(closedOrders, orient='index')
        df['txId'] = df.index
        return df

    def tradesHistory(self, start=None, end=None) -> DataFrame:
        data = {}
        if start:
            data['start'] = start
        if end:
            data['end'] = end
        response = self.kapi.query_private("TradesHistory", data)
        df = DataFrame.from_dict(response['result']['trades'], orient='index')
        df['txId'] = df.index
        return df

    def addorder (self, order: dict) :
        try:
            return self.kapi.query_private("AddOrder", order)
        except (HTTPError):
            return None


