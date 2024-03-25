# -*- coding: utf-8 -*-
from flask import Flask
from server.src.utils.common import register_blueprints
from server.src.settings import config

def create_app(config_type, package_name, package_path):
    app = Flask(__name__, instance_relative_config=True)
    app_settings = config[config_type]
    app.config.from_object(app_settings)

    register_blueprints(app, package_name, package_path)

    return app