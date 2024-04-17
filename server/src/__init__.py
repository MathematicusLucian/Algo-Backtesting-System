# -*- coding: utf-8 -*-
from flask import Flask
from src.utils.common import register_blueprints
from src.settings import config

# # -*- coding: utf-8 -*-
# from flask import Flask
# from src.utils.utils import save_dataframe
# # from src.services.db.db import create_connection, is_table
# from src.utils.common import register_blueprints
# from settings import config
# from .utils import *

# save_dataframe = save_dataframe
# # create_connection = create_connection
# # is_table = is_table

# # market data
# order_books = {}
# instruments = {}
# tickers_container = []
# mark_px_container = []

# # position management
# balance_and_position_container = []
# account_container = []
# positions_container = []

# # order management
# orders_container = []

def create_app(config_type, package_name, package_path):
    app = Flask(__name__, instance_relative_config=True)
    print('config[config_type]',config[config_type])
    app_settings = config[config_type]
    app.config.from_object(app_settings)
    register_blueprints(app, package_name, package_path)
    return app