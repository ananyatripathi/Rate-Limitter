from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Handling CORS like in FastAPI

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"Hello": "World"})

if __name__ == '__main__':
    app.run(debug=True)
