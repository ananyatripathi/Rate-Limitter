import time
from threading import Lock

class FixedWindowCounter:
    def __init__(self, max_number_req, time_interval):
        self.max_number_req = max_number_req
        self.time_interval = time_interval
        self.req_arr = []
        self.lock = Lock()
    
    def handle_request(self):
        with self.lock:
            if(len(self.req_arr)<self.max_number_req):
                self.req_arr.append(time.time())
                return True
            else:
                return False
    
    def handle_new_timeframe(self):
        self.req_arr = []
        return len(self.req_arr)
        
        

