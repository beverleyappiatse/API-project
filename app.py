from flask import Flask, jsonify, request
from datetime import datetime
import pytz

app = Flask(__name__)

# Secure token
API_TOKEN = "supersecrettoken123"

#  Dictionary of capital cities and their time zones
capital_timezones = {
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "New Delhi": "Asia/Kolkata",
    "Canberra": "Australia/Sydney",
    "Brasília": "America/Sao_Paulo",
    "Ottawa": "America/Toronto",
    "Cairo": "Africa/Cairo",
    "Beijing": "Asia/Shanghai"
}

# Auth decorator
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized access. Valid token required."}), 401
    decorator.__name__ = f.__name__
    return decorator

# Time API
@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    capital = request.args.get('capital')
    if not capital:
        return jsonify({"error": "Please provide a capital city using the 'capital' query parameter."}), 400

    timezone_str = capital_timezones.get(capital)
    if not timezone_str:
        return jsonify({"error": f"'{capital}' is not in our database. Please try another capital."}), 404

    timezone = pytz.timezone(timezone_str)
    local_time = datetime.now(timezone)
    offset = local_time.strftime('%z')
    offset_formatted = f"UTC{'+' if int(offset) >= 0 else ''}{int(offset) // 100}"

    return jsonify({
        "capital": capital,
        "timezone": timezone_str,
        "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
        "utc_offset": offset_formatted
    })

# Hello endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from your time API!"})

# Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
