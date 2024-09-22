import time
from threading import Lock
class SlidingWindowLog:
    def __init__(self, max_req_allowed, time_window):
        self.max_req_allowed=max_req_allowed
        self.time_window=time_window
        self.lock=Lock()
        self.req_arr=[]
        self.removed_timestamps = []
        self.outdated_timestamps = []
    
    def handle_request(self):
        with self.lock:
            current_time = time.time()
            # Separate the valid and outdated timestamps
            valid_timestamps = []
            self.outdated_timestamps = []
            
            for timestamp in self.req_arr:
                if current_time - timestamp <= self.time_window:
                    valid_timestamps.append(timestamp)
                else:
                    self.outdated_timestamps.append(timestamp)
            
            # Update the request array and store the removed timestamps
            self.req_arr = valid_timestamps
            self.removed_timestamps.extend(self.outdated_timestamps)

            # Check if the new request can be added
            if len(self.req_arr) < self.max_req_allowed:
                self.req_arr.append(current_time)
                return True
            else:
                return False

