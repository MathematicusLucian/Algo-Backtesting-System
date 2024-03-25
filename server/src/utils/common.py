# -*- coding: utf-8 -*-
import pkgutil
import importlib
from flask import Blueprint
from dotenv import dotenv_values

def register_blueprints(app, package_name, package_path):
    """
    :return rv (list): list of blueprints
    """
    blue_prints = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        files = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(files):
            item = getattr(files, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            blue_prints.append(item)
    return blue_prints

def get_config():
    config = dotenv_values("../../../.env")
    return config['LIVECOINWATCH_API_KEY']