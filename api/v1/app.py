#!/usr/bin/python3
"""app file"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()


@app.errorhandler(404)
def error_handle(error):
    """returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
