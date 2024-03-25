# -*- coding: utf-8 -*-
import os
from src.api import create_app_blueprint

application = create_app_blueprint(os.getenv('FLASK_CONFIG') or 'default')