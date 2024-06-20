from flask import Flask, request, jsonify
import json
from flask_swagger_ui import get_swaggerui_blueprint
from .blueprints import endpoints_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(endpoints_blueprint)

    return app

# SWAGGER_URL = '/swagger'
# API_URL = 'http://127.0.0.1:5000/swagger.json'
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Sample API"
#     }
# )
# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
#
# @app.route('/swagger.json')
# def swagger():
#     with open('swagger.json', 'r') as f:
#         return jsonify(json.load(f))
