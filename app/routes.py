from flask import Blueprint, request, jsonify
from .utils import is_potentially_unsanitized

# Using Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/v1')

@api_bp.route('/sanitized/input/', methods=['POST'])
def check_sanitization():
    #API ENDPOINT

    # 1. Check if the request content type is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415 # Unsupported Media

    # 2. Try to parse JSON data
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": f"Invalid JSON received: {e}"}), 400 # Bad Request

    # 3. Check if 'input' key exists and is a string
    if not data or 'input' not in data:
        return jsonify({"error": "Missing 'input' key in JSON payload"}), 400

    input_string = data['input']

    if not isinstance(input_string, str):
         return jsonify({"error": "'input' value must be a string"}), 400

    # 4. Perform the sanitization check 
    if is_potentially_unsanitized(input_string):
        result = {"result": "unsanitized"}
    else:
        result = {"result": "sanitized"}

    # 5. Return the result
    return jsonify(result), 200
    