# -*- coding: utf-8 -*-
from src.services.market_data_service import BaseService
from src.services.market_data_service import CoinDataService

# # -*- coding: utf-8 -*-
# from src.utils.utils import save_dataframe
# # from src.services.db.db import create_connection, is_table
# from flask import Flask
# from src.utils.common import register_blueprints
# from settings import config

# def create_app(config_type, package_name, package_path):
#     app = Flask(__name__, instance_relative_config=True)
#     print('config[config_type]',config[config_type])
#     app_settings = config[config_type]
#     app.config.from_object(app_settings)
#     register_blueprints(app, package_name, package_path)
#     return app

# save_dataframe = save_dataframe
# # create_connection = create_connection
# # is_table = is_table


# # from flask import Blueprint, Flask, flash, redirect, url_for
# # # from flask_login import current_user
# # # from src.services.flask_setup_service import FlaskSetupService
# # # from flask_sock import Sock
# # from settings import config
# # from src.utils.common import get_config, register_blueprints
# # # from .sentiment_service import *
# # # from .x_service import x_archive
# # # from .scraping_service import *
# # # from .crypto_analysis import *
# # from .metals_data_service import *
# # from src.endpoints.rest import algo_rest_blueprint

# # # def create_app(config_type, package_name, package_path):
# # #     flask_setup = Flask(__name__, instance_relative_config=True)
# # #     app = FlaskSetupService(flask_setup, test_config=None, config_type=None, package_name=None, package_path=None)
# # #     app.run(debug=True, port=5000)
# # #     return app
# #     # register_blueprints(app, package_name, package_path)

# # def create_app_blueprint(config): #Flask app as RMIS instance
# #     # return create_app(config, __name__, __path__)
# #     app = Flask(__name__)
# #     app.register_blueprint(algo_rest_blueprint)
# #     app.run(debug=True)