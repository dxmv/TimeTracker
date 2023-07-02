class Action:
    def __init__(self, start, end, text,date):
        self.start = start
        self.end = end
        self.text = text
        self.date=date

    def __init__(self, start, end,date):
        self.start = start
        self.end = end
        self.text = None
        self.date = date

    def set_text(self,text):
        self.text=text
