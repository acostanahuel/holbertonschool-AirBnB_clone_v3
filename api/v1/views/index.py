#!/usr/bin/python3
"""
Flask Blueprint
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ status endopint """
    return jsonify({"status": "OK"})
