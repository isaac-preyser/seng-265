class Note: 
    def __init__(self, code, text, timestamp):
        self.code = code
        self.text = text
        self.timestamp = timestamp
    
    def __eq__(self, other):
        return self.code == other.code and self.text == other.text and self.timestamp == other.timestamp
    
    def __str__(self):
        return f'{self.code} - {self.text} : {self.timestamp}'
    