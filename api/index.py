from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from app.token_bucket import TokenBucket
from app.leaking_bucket import LeakingBucket
from app.fixed_window_counter import FixedWindowCounter
from app.sliding_window_log import SlidingWindowLog
from typing import Optional


app = Flask(__name__)
CORS(app)  # Handling CORS like in FastAPI

# Initialize global variables for rate-limiter objects
token_bucket: Optional[TokenBucket] = None
leaking_bucket: Optional[LeakingBucket] = None
fixed_window_counter: Optional[FixedWindowCounter] = None
sliding_window_log: Optional[SlidingWindowLog] = None

# Pydantic Models
class TokenBucketModel(BaseModel):
    capacity: int
    refill_rate_per_minute: int

class LeakingBucketModel(BaseModel):
    bucket_size: int
    outflow_rate_per_minute: int

class FixedWindowCounterModel(BaseModel):
    max_number_req: int
    time_interval: int

class SlidingWindowLogModel(BaseModel):
    max_req_allowed: int
    time_window: int

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


########################################## LEAKING BUCKET ALGORITHM #################################################

@app.route("/setup_leaking_bucket", methods=["POST"])
def setup_leaking_bucket():
    try:
        data = request.json
        params = LeakingBucketModel(**data)
        global leaking_bucket
        leaking_bucket = LeakingBucket(bucket_size=params.bucket_size, outflow_rate_per_minute=params.outflow_rate_per_minute)
        return jsonify({"status": "bucket initialized", "bucket_size": params.bucket_size, "outflow_rate_per_minute": params.outflow_rate_per_minute}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 422

@app.route("/add_request_to_q", methods=["POST"])
def add_request_to_queue():
    if leaking_bucket is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    if leaking_bucket.add_request():
        return jsonify({"status": "Request Added to Queue", "queue_size": len(leaking_bucket.queue)}), 200
    else:
        return jsonify({"status": "Queue is Full, Request Dropped", "queue_size": len(leaking_bucket.queue)}), 429

@app.route("/process_requests", methods=["POST"])
def process_requests():
    if leaking_bucket is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    result = leaking_bucket.process_requests()
    return jsonify(result), 200


########################################## FIXED WINDOW COUNTER ALGORITHM #################################################

@app.route("/setup_fixed_window_counter", methods=["POST"])
def setup_fixed_window_counter():
    try:
        data = request.json
        params = FixedWindowCounterModel(**data)
        global fixed_window_counter
        fixed_window_counter = FixedWindowCounter(max_number_req=params.max_number_req, time_interval=params.time_interval)
        return jsonify({"status": "bucket initialized", "max_number_req": params.max_number_req, "time_interval": params.time_interval}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 422

@app.route("/handle_request_fixed_window_counter", methods=["POST"])
def handle_request_fixed_window_counter():
    if fixed_window_counter is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    if fixed_window_counter.handle_request():
        return jsonify({"status": "Request Accepted", "num_of_request": len(fixed_window_counter.req_arr)}), 200
    else:
        return jsonify({"status": "Request Rejected", "num_of_request": len(fixed_window_counter.req_arr)}), 429

@app.route("/handle_new_timeframe", methods=["POST"])
def handle_new_timeframe():
    if fixed_window_counter is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    updated_req_arr = fixed_window_counter.handle_new_timeframe()
    return jsonify({"updated_req_arr": updated_req_arr}), 200


########################################## SLIDING WINDOW LOG ALGORITHM #################################################

@app.route("/setup_sliding_window_log", methods=["POST"])
def setup_sliding_window_log():
    try:
        data = request.json
        params = SlidingWindowLogModel(**data)
        global sliding_window_log
        sliding_window_log = SlidingWindowLog(max_req_allowed=params.max_req_allowed, time_window=params.time_window)
        return jsonify({"status": "bucket initialized", "max_req_allowed": params.max_req_allowed, "time_window": params.time_window}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 422

@app.route("/handle_request_sliding_window_log", methods=["POST"])
def handle_request_sliding_window_log():
    if sliding_window_log is None:
        return jsonify({"error": "Bucket not initialized"}), 400
    if sliding_window_log.handle_request():
        return jsonify({
            "status": "Request Accepted",
            "num_of_request": len(sliding_window_log.req_arr),
            "outdated_req": len(sliding_window_log.outdated_timestamps),
            "timestamps": sliding_window_log.req_arr,
            "outdated_timestamps": sliding_window_log.outdated_timestamps
        }), 200
    else:
        return jsonify({
            "status": "Request Rejected",
            "num_of_request": len(sliding_window_log.req_arr),
            "outdated_req": len(sliding_window_log.outdated_timestamps),
            "timestamps": sliding_window_log.req_arr,
            "outdated_timestamps": sliding_window_log.outdated_timestamps
        }), 429

if __name__ == '__main__':
    app.run(debug=True)
