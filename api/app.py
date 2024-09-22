from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import mimetypes

app = Flask(__name__)
CORS(app)

USER_ID = "john_doe_17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

@app.route('/bfhl', methods=['POST'])
def bfhl_post():
    try:
        data = request.json.get('data')
        file_b64 = request.json.get('file_b64')

        # Validate input
        if not isinstance(data, list):
            return jsonify({"is_success": False, "message": "Invalid input format"}), 400

        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha() and len(item) == 1]
        
        # Find the highest lowercase alphabet
        lowest_alphabet = [char for char in alphabets if char.islower()]
        highest_lowercase_alphabet = sorted(lowest_alphabet)[-1:] if lowest_alphabet else []

        # File handling
        file_valid = False
        file_mime_type = None
        file_size_kb = None
        
        if file_b64:
            try:
                # Decode the base64 string
                file_data = base64.b64decode(file_b64)
                # Determine the MIME type and size
                file_mime_type = mimetypes.guess_type(file_b64)[0]
                file_size_kb = len(file_data) / 1024  # Size in KB
                file_valid = True
            except Exception as e:
                file_valid = False

        return jsonify({
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lowercase_alphabet,
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": file_size_kb
        })

    except Exception as e:
        return jsonify({"is_success": False, "message": str(e)}), 500


@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    return jsonify({"operation_code": 1})

if __name__ == '__main__':
    app.run(debug=True)
