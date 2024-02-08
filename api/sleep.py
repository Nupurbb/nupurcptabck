from flask import Flask, Blueprint, jsonify
import pandas as pd
from flask_cors import CORS
import os
from flask_restful import Api, Resource  # Import Api and Resource

# Create a single Flask application
app = Flask(__name__)

# Create a blueprint for the API
sleep_api = Blueprint('sleep_api', __name__, url_prefix='/api/sleep')
api_sleep = Api(sleep_api)

CORS(sleep_api)

class SleepDataAPI(Resource):
    def get(self):
        # Get the path to the sleep database
        app_root = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(app_root, 'api', 'sleep.csv')
        print("App Root:", app_root)
        print("CSV Path:", csv_path)
        
        try:
            data_sleep = pd.read_csv(csv_path)
        except FileNotFoundError:
            return {"error": "File not found"}, 404


        if data_sleep.empty:
            return jsonify({"error": "Data not available"}), 404

        return jsonify(data_sleep.to_dict(orient='records'))

# Register the resource with the api_sleep object
api_sleep.add_resource(SleepDataAPI, '/')

# Register the blueprint with the Flask app
app.register_blueprint(sleep_api)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
