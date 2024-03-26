# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from src.utils.common import get_config
from src.services.coindata import CoinDataService

api_key = get_config('LIVECOINWATCH_API_KEY')
base_currency = get_config('BASE_CURRENCY')
coins = get_config('COINS')
coin_data = CoinDataService(api_key, base_currency)
route = Blueprint('default', __name__)

@route.route("/api")
def helloworld():
    return jsonify({"status": 200, "msg":"CryptoTracker Flask API"})

@route.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg":"I am the CryptoTracker Flask API"})

# /api/currencies?selected=GBP
@route.route("/api/currencies")
def currencies():
    selected_currency = request.args.get('selected') if request.args.get('selected') else None
    currencies = coin_data.get_currencies(selected_currency)
    return jsonify({"res": currencies})

# /api/currencies?base=GBP&second_currency=BTC
@route.route("/api/coin_history")
def historic_values__coin():
    base = request.args.get('base')
    second_currency = request.args.get('second_currency')
    period = request.args.get('period')
    return coin_data.get_historic_values__coin(second_currency, base)

@route.route("/api/coins_history")
def historic_values__coins():
    return coin_data.get_historic_values__coins(coins)

@route.route("/api/latest_values")
def latest_values():
    return coin_data.get_latest_values(coins)