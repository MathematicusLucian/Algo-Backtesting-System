# -*- coding: utf-8 -*-
from markupsafe import escape
from flask import abort, app, Blueprint, jsonify, redirect, render_template, request, url_for
from src.utils.common import get_config

# api_key = get_config('')
route = Blueprint('default', __name__)

# @route.errorhandler(404)
# def not_found():
#     return redirect(url_for('not_found'))

# @route('/not-found')
# def page_not_found(error):
#     abort(404)

# --------------------
# ------- ROOT -------
# --------------------    
# http://127.0.0.1:5000/
@route.route("/")
# @cache.cached(timeout=60)
def index():
    version = "v1.0.0"
    return jsonify({"MDI API -/" : format(escape(version))})

@route.route("/api")
def helloworld():
    return jsonify({"status": 200, "msg":"MDI API"})

@route.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg":"You pinged the MDI API"})