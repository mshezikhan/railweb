from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithm import planner

app = Flask(__name__)
CORS(app)

@app.route('/find-route', methods=['POST'])
def get_route():
    data = request.get_json() or {}
    source = data.get('source', '').strip()
    dest = data.get('destination', '').strip()

    if not source or not dest:
        return jsonify({"error": "source and destination are required"}), 400

    routes = planner.find_routes(source, dest)
    return jsonify({"routes": routes})


if __name__ == '__main__':
    app.run(debug=True)