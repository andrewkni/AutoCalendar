import datetime as dt

# Event
class Event:
    def __init__(self, title, everyday=False, priority=None, duration=None, start=None, end=None, fixed=False):
        # rename event to Untitled if no name
        if not title:
            title = 'Untitled'

        self.title = title
        self.fixed = fixed
        self.everyday = everyday

        # conflict (fixed time)
        if self.fixed:
            self.priority = 6
            self.start = start
            self.end = end
        # task (unfixed time)
        else:
            self.duration = duration
            self.priority = priority

    def print_event(self):
        if self.fixed:
            return (
                f"{self.title}  \n"
                f"Start: {self.start}  \n"
                f"End: {self.end}"
            )
        else:
            return (
                f"{self.title}  \n"
                f"Priority: {self.priority}\n"
                f"Duration: {self.duration}"
            )

    # Exports event to be created in Google Calendar
    def __call__(self):
        event = {
            'summary': self.title,
            'start': {
                'dateTime': self.start,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': self.end,
                'timeZone': 'America/Los_Angeles',
            },
        }

        return event

    def get_start_dt(self):
        return self.start

    def get_end_dt(self):
        return self.end