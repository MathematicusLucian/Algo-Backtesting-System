# -*- coding: utf-8 -*-
from jinja2 import TemplateNotFound
from markupsafe import escape
from flask import abort, app, Blueprint, jsonify, redirect, render_template, abort, request, url_for
from src.utils.common import get_config
# from src.models import Backtest

# api_key = get_config('')
backtesting_bp = Blueprint('backtesting_bp', __name__,
    template_folder='templates')
# backtesting_bp = Blueprint('backtesting_bp', __name__,
#     template_folder='templates',
#     static_folder='static', static_url_path='assets')

# @backtesting_bp.errorhandler(404)
# def not_found():
#     return redirect(url_for('not_found'))

# @backtesting_bp('/not-found')
# def page_not_found(error):
#     abort(404)

# --------------------
# ------- ROOT -------
# --------------------    
# http://127.0.0.1:5000/
@backtesting_bp.route("/", defaults={'page': 'index'})
@backtesting_bp.route("/api")
@backtesting_bp.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)

@backtesting_bp.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg":"You pinged the Backtesting API"})