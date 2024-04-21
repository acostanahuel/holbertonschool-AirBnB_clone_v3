"""
Flask API
"""
from flask import Flask, render_template
app = Flask(__name__)
from models import storage
from views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def app_close(exception=None):
    """ Teardown method """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
