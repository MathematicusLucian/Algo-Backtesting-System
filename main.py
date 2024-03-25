from dotenv import dotenv_values
from src.coindata import CoinData

def get_api_key():
    config = dotenv_values(".env")
    return config['LIVECOINWATCH_API_KEY']

if __name__ == '__main__':

    api_key = get_api_key()
    base_currency = "GBP"
    coin_data = CoinData(api_key, base_currency)
    coins = ["ETH","BTC","XRP","SHIB"]

    history = coin_data.historic_values(coins)
    print(history)

    latest = coin_data.latest_values(coins)
    print(latest)