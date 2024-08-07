#!/usr/bin/python3
"""
Flask API
"""
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def app_close(exception=None):
    """ Teardown method """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and return JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
