class OrderBuilder:

    VAlID_ORDER_TYPE = ['market', 'limit', 'stop-loss', 'take-profit', 'stop-loss-limit', 'take-profit-limit', 'settle-position']


    def __init__(self, pair: str):
        self.order = {}
        self.pair(pair)

    def pair (self, assetPair):
        self.order['pair'] = assetPair
        return self

    def type (self, type: str):
        assert (type in ['buy', 'sell']), "type must be buy/sell"
        self.order['type']  = type
        return self

    def ordertype (self, ordertype: str):
        assert (ordertype in self.VAlID_ORDER_TYPE), "ordertype must be one of {}".format(self.VAlID_ORDER_TYPE)
        self.order['ordertype'] = ordertype
        return self

    def price (self, price):
        self.order['price'] = price
        return self

    def price2 (self, price2):
        self.order['price2'] = price2
        return self

    def volume (self, volume):
        self.order['volume'] = volume
        return self

    def leverage(self, leverage):
        self.order['leverage'] = leverage
        return self

    def oflags (self, oflags:str):
        flags = oflags.split(",")
        for flag in flags:
            assert (flag in ['fcib','fciq','nompp','post']), "oflags must be one of {}".format(['fcib','fciq','nompp','post'])
        self.order['oflags'] = oflags
        return self

    def starttm (self, starttm:str):
        self.order['starttm'] = starttm
        return self

    def expiretm (self, expiretm:str):
        self.order['expiretm'] = expiretm
        return self

    def userref (self, userref):
        self.order['userref'] = userref
        return self

    def validate (self, validate:bool = True):
        self.order['validate'] = validate
        return self

    def build (self):
        assert (self.order['pair']), "Pair required"
        assert (self.order['ordertype'] != 'market' or self.order['price']), "Price required for no market order type"
        if self.order['ordertype'] in ["stop-loss-limit", "take-profit-limit"]:
            assert (self.order['price'] and self.order['price2']), "{} requires price and price2".format(self.order['ordertype'])
        assert(self.order['volume']), "Volume required"
        assert (self.order['type']), "Buy/sell type required"
        return self.order