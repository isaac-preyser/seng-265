import datetime

class Note: 
    def __init__(self, code, text):
        self.code = code
        self.text = text
        self.timestamp = datetime.datetime.now()
    
    def __eq__(self, other):
        return self.code == other.code and self.text == other.text
    
    def update(self, text):
        self.text = text
        self.timestamp = datetime.datetime.now()
        return self
    
    def create(code, text):
        return Note(code, text)
    
    def __str__(self):
        return f'{self.code} - {self.text} : {self.timestamp}'
    