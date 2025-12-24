import datetime as dt

# Time Range
class TimeRange:
    def __init__(self, start, end):

        self.start = start
        self.end = end

    def get_duration(self):
        return (self.end - self.start).total_seconds() / 60

    def print_time_range(self):
        print(f"{self.start.strftime('%Y-%m-%d %H:%M:%S')} to {self.end.strftime('%Y-%m-%d %H:%M:%S')}")

    # Removes a certain amount of time from the start of the time range
    def remove_time(self, time):
        self.start += dt.timedelta(minutes=time)
