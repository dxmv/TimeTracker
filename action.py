class Action:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.text = None
