import datetime

class Note: 
    def __init__(self, code, text):
        self.code = code
        self.text = text
        self.timestamp = datetime.datetime.now()
    
    def __eq__(self, other):
        time_difference = abs((self.timestamp - other.timestamp).total_seconds())
        return self.code == other.code and self.text == other.text and time_difference <= 10
        #times between tester and expected values are not EXACTLY the same. 10 seconds should be enough (in terms of execution time between setup and testing)
        #HOWEVER, this is NOT a good solution for a real-world application. Different machines and environments will have different execution times. (and 10 seconds is a long time for a computer)

    def __str__(self):
        return f'{self.code} - {self.text} : {self.timestamp}'
    
    def update(self, text):
        self.text = text
        self.timestamp = datetime.datetime.now()
        return self
    
    def create(code, text):
        return Note(code, text)
    