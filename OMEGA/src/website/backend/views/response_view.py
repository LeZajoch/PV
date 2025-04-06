from flask import jsonify

def success_view(prediction):
    return jsonify({"prediction": prediction})

def error_view(message):
    return jsonify({"error": message})
