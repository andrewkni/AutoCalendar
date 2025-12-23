import datetime as dt

# Event
class Event:
    def __init__(self, title, priority=None, duration=None, date=None, start=None, end=None, fixed=False):
        # rename event to Untitled if no name
        if not title:
            title = 'Untitled'

        self.title = title
        self.fixed = fixed

        # conflict
        if self.fixed:
            self.date = date
            self.priority = 6
            self.start = dt.datetime.combine(date, start)
            self.end = end
        # task
        else:
            self.duration = duration
            self.priority = priority

    def print_event(self):
        if self.fixed:
            return (
                f"Name: {self.title}\n"
                f"Date: {self.date}\n"
                f"Start: {self.start}\n"
                f"End: {self.end}"
            )
        else:
            return (
                f"Name: {self.title}\n"
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