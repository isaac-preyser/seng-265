from datetime import datetime

class PatientRecord:
    def __init__(self):
        self.notes = [] #contains a list of notes. 
        self.auto_counter = 0 #counts number of notes in the record. 

    def __eq__(self, other):
        return self.notes == other.notes and self.auto_counter == other.auto_counter
    
    
    def add_note(self, note):
        self.notes.append(note)
        self.auto_counter += 1

    def remove_note(self, note):
        self.notes.remove(note)
        self.auto_counter -= 1
    
