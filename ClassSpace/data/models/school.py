class School:

    def __init__(self, name: str, tz_offset: str):
        self.id = None
        self.name = name
        self.tz_offset = tz_offset

    def __str__(self):
        return self.name
