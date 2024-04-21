from livecoinwatch import LiveCoinWatch
from datetime import datetime, timedelta
from src.services.market_data_service.base import BaseService

class CoinDataService(BaseService):

    def __init__(self, api_key, base_currency):
        super().__init__(api_key, base_currency)
        self.currencies = [{"name":"Pounds Sterling", "code":"GBP"}, 
                           {"name":"United States Dollars", "code":"USD"}, 
                           {"name":"Bitcoin", "code":"BTC"}, 
                           {"name":"Ethereum", "code":"ETH"}, 
                           {"name":"Solana", "code":"SOL"}, 
                           {"name":"Ripple", "code":"XRP"}, 
                           {"name":"Shiba Inu", "code":"SHIB"}, 
                           {"name":"Dogecoin", "code":"DOGE"}]
        self.coin_data_api = LiveCoinWatch(api_key, base_currency) 

    def set_base_currency(self, currency):
        self.base_currency = currency

    def get_currencies(self, selected_currency):
        x = [i for i in self.currencies if i != selected_currency]
        print(x)
        return x

    # Call 'coins/single/history'
    def get_historic_values__coin(self, second_currency, base, days_back):
        base_currency = base if base!=None else self.base_currency
        period_start = (datetime.today() - timedelta(days=(days_back))).timestamp() * 1000
        period_end = (datetime.today()).timestamp() * 1000
        return self.coin_data_api.coin__history(code=second_currency,currency=base_currency,start=period_start,end=period_end)

    # Call 'coins/single/history'
    def get_historic_values__coins(self, coins):
        historic_values = []
        for coin in coins:
            coin_history = self.coin_data_api.coin__history(code=coin,currency=self.base_currency,start=1617035100000,end=1617035400000)
            historic_values.append(coin_history)
        return historic_values

    # Call 'coins/map'
    def get_latest_values(self, coins):
        return self.coin_data_api.coins__map(codes=coins, currency=self.base_currency, sort="rank", offset=0, limit=0)
   
    # historic_values = []
    # for i in range(1,(days_back+1))[::-1]:
    #     period_start = (datetime.today() - timedelta(days=(i))).timestamp() * 1000
    #     period_end = (datetime.today() - timedelta(days=(i-1))).timestamp() * 1000
    #     day_range = self.coin_data_api.coin__history(code=second_currency,currency=base_currency,start=period_start,end=period_end)
    #     historic_values.append(day_range)