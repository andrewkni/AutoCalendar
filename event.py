class Event:
    def __init__(self, title, priority, duration):
        self.title = title
        self.priority = priority
        self.duration = duration

        self.start = 0
        self.end = 0

    def print_event(self):
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