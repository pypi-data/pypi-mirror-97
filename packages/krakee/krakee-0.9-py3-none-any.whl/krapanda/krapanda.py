import krakenex

from krapanda.api.PrivateApi import PrivateApi
from krapanda.api.PublicApi import PublicApi


class Krapanda:

    def __init__(self, authfile=None):
        self.kapi = krakenex.API()
        if authfile:
            self.kapi.load_key(authfile)
            self.__privateApi = PrivateApi(self.kapi)
        else:
            self.__privateApi = None
        self.__publicApi = PublicApi(self.kapi)
        self.cache = {}
        self.cache['assetPairs'] = self.public().asset_pairs()

    def public(self) -> PublicApi:
        return self.__publicApi

    def private(self) -> PrivateApi:
        if not self.__privateApi:
            raise Exception("Private methods disabled. Please provide credentials file when creating: Kapi(<path>)")
        return self.__privateApi

