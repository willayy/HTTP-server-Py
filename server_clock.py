from datetime import datetime, timedelta


class ServerClock:
    def __init__(self):
        self.birth = datetime.now()
        
    def get_up_time_sec(self):
        return timedelta.total_seconds(datetime.now() - self.birth)