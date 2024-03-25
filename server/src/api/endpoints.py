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
    return "CryptoTracker Flask API"

@route.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg":"I am the CryptoTracker Flask API"})

@route.route("/api/historic_values")
def historic_values():
    return coin_data.historic_values(coins)

@route.route("/api/latest_values")
def latest_values():
    return coin_data.latest_values(coins)