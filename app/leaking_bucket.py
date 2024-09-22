from collections import deque
import time
from threading import Lock

class LeakingBucket:
    def __init__(self, bucket_size, outflow_rate_per_minute):
        self.bucket_size=bucket_size
        self.outflow_rate_per_minute=outflow_rate_per_minute
        self.queue=deque()
        self.lock = Lock()
    
    def add_request(self):
        with self.lock:
            if len(self.queue) < self.bucket_size:
                self.queue.append(time.time())
                return True
            else:
                return False
    
    def process_requests(self):
        processed_req=0
        with self.lock:
            if self.queue:
                while self.queue and processed_req < self.outflow_rate_per_minute:
                    request_time = self.queue.popleft()
                    processed_req += 1
        return {"queue_size":len(self.queue), "processed_request":processed_req}
                    



