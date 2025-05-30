from flask import Flask, request, jsonify
import time
from collections import defaultdict

app = Flask(__name__)

# Token bucket settings
MAX_TOKENS = 3
REFILL_RATE = 2  # tokens per second
TOKEN_BUCKET = defaultdict(lambda: {'tokens': MAX_TOKENS, 'last_check': time.time()})

# Counters
total_requests = 0
served_requests = 0
blocked_requests = 0

@app.route('/')
def home():
    global total_requests, served_requests, blocked_requests

    ip = request.remote_addr
    total_requests += 1

    now = time.time()
    bucket = TOKEN_BUCKET[ip]

    # Refill tokens
    elapsed = now - bucket['last_check']
    refill = int(elapsed * REFILL_RATE)
    if refill > 0:
        bucket['tokens'] = min(MAX_TOKENS, bucket['tokens'] + refill)
        bucket['last_check'] = now

    # Try to serve request
    if bucket['tokens'] > 0:
        bucket['tokens'] -= 1
        served_requests += 1
        return "Request served successfully", 200
    else:
        blocked_requests += 1
        return "Too many requests", 429

@app.route('/stats')
def stats():
    return jsonify({
        "Total Requests": total_requests,
        "Served": served_requests,
        "Blocked": blocked_requests
    })

if __name__ == '__main__':
    app.run(port=5000)
