import time

class Timer:
    def __init__(self, events):
        self.events_completed = 0
        self.start_time = time.time()
        self.total_events = events

    def update(self):
        self.events_completed += 1
        self.time_elapsed = time.time()-self.start_time
        percentage = self.events_completed/self.total_events
        self.total_time = self.time_elapsed/percentage
        return f"{100*percentage:.1f}% complete: {self.time_elapsed:.1f}s"

    def final_time(self):
        end_time = time.time()-self.start_time
        minutes = end_time//60
        seconds = end_time%60
        return f"{minutes} minutes, {seconds} seconds"