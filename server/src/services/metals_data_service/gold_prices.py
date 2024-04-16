import requests
# import pandas_datareader as fred 
# # https://fred.stlouisfed.org/docs/api/fred/
# # https://fred.stlouisfed.org/docs/api/fred/category.html
# # https://fred.stlouisfed.org/docs/api/fred/series_categories.html
# import fredpy as fredpy
# # https://www.briancjenkins.com/fredpy/docs/build/html/index.html
# # https://www.briancjenkins.com/fredpy/docs/build/html/fredpy_examples.html#Preliminary-example 
# # https://www.briancjenkins.com/fredpy/docs/build/html/fredpy_examples.html#A-closer-look-at-fredpy-using-real-GDP-data
# from fred import FredAPI
# # https://github.com/zachspar/fred-py-api
# # https://fred-py-api.readthedocs.io/en/latest/
from src.utils.utils import get_envar

# def get_historic_gold_prices(fromDate): #19000101
#     fredpy.api_key = get_envar("FRED_API_KEY")
#     gold = fredpy.series('XAU')
#     # return fred.DataReader("GOLDAMGBD228NLBM", data_source="fred", start=fromDate)
#     fred_client = FredAPI(get_envar("FRED_API_KEY"))
#     fred_client.get_category()
#     fred_client.get_series_observations("XAU")

def fetch_gold_price(timestamp, base_curr, symbol):
    api_key = get_envar("GOLDAPIIO_KEY")
    print(timestamp)
    url = f"https://www.goldapi.io/api/{symbol}/{base_curr}{timestamp}"
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.text
        return result
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"