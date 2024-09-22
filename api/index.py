from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from app.token_bucket import TokenBucket
from typing import Optional


app = Flask(__name__)
CORS(app)  # Handling CORS like in FastAPI

token_bucket: Optional[TokenBucket] = None

# Pydantic Models
class TokenBucketModel(BaseModel):
    capacity: int
    refill_rate_per_minute: int

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"Hello": "World"})

########################################## TOKEN BUCKET ALGORITHM #################################################

@app.route("/setup_token_bucket", methods=["POST"])
def setup_token_bucket():
    try:
        data = request.json
        params = TokenBucketModel(**data)  # Validate request data using Pydantic
        global token_bucket
        token_bucket = TokenBucket(capacity=params.capacity, refill_rate_per_minute=params.refill_rate_per_minute)
        return jsonify({"status": "Bucket Initialized", "capacity": params.capacity, "refill_rate_per_minute": params.refill_rate_per_minute}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 422

@app.route("/handle_token_bucket", methods=["POST"])
def handle_token_bucket():
    if token_bucket is None:
        return jsonify({"error": "Bucket Not Initialized"}), 400
    if token_bucket.handle_request():
        return jsonify({"status": "accepted", "tokens": token_bucket.tokens}), 200
    else:
        return jsonify({"status": "rejected", "tokens": token_bucket.tokens}), 429

@app.route("/refill", methods=["POST"])
def api_refill():
    if token_bucket is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    updated_tokens = token_bucket.refill()  # Trigger the refill process
    return jsonify({"status": "bucket refilled", "tokens": updated_tokens}), 200


if __name__ == '__main__':
    app.run(debug=True)
