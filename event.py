class Event:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

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