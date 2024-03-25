from livecoinwatch import LiveCoinWatch

class CoinData:

    def __init__(self, api_key, base_currency):
        self.api_key = api_key
        self.base_currency = base_currency
        self.coin_data_api = LiveCoinWatch(api_key, base_currency) 

    def set_base_currency(self, currency):
        self.base_currency = currency

    # Call 'coins/single/history'
    def historic_values(self, coins):
        historic_values = []
        for coin in coins:
            coin_history = self.coin_data_api.coin__history(code=coin,currency=self.base_currency,start=1617035100000,end=1617035400000)
            historic_values.append(coin_history)
        return historic_values

    # Call 'coins/map'
    def latest_values(self, coins):
        return self.coin_data_api.coins__map(codes=coins, currency=self.base_currency, sort="rank", offset=0, limit=0)
   