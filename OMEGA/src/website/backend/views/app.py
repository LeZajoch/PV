# website/backend/views/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the parent directory to sys.path to import the controller
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ..controllers.predict_controller import PredictController

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize controller
predict_controller = PredictController()


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint to predict team car performance"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    result, status_code = predict_controller.predict_performance(data)

    return jsonify(result), status_code


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "API is running"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
