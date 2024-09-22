from threading import Lock

class TokenBucket:
    def __init__(self, capacity, refill_rate_per_minute):
        self.capacity = capacity
        self.refill_rate_per_minute = refill_rate_per_minute
        self.tokens = capacity
        self.lock = Lock()
    
    def refill(self):
        self.tokens = min(self.capacity, self.tokens + self.refill_rate_per_minute)
        return self.tokens
    
    def handle_request(self):
        with self.lock:
            if self.tokens > 0:
                self.tokens -= 1
                return True
            else:
                return False
