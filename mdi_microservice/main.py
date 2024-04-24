from src.utils.common import get_config
from src.services.market_data_service.coindata import CoinDataService

if __name__ == '__main__':

    api_key = get_config('LIVECOINWATCH_API_KEY')
    base_currency = get_config('BASE_CURRENCY')
    coins = get_config('COINS')
    coin_data = CoinDataService(api_key, base_currency)

    history = coin_data.historic_values(coins)
    print(history)

    latest = coin_data.latest_values(coins)
    print(latest)