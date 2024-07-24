from flask import Flask, jsonify
import json
from flask_swagger_ui import get_swaggerui_blueprint
from app.blueprints import endpoints_blueprint
from flask_cors import CORS



SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


app.register_blueprint(endpoints_blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)