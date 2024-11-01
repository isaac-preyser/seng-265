from clinic.note import Note

class PatientRecord:
    def __init__(self):
        self.notes = [] #contains a list of notes. 
        self.auto_counter = 0 #counts number of notes in the record. 

    def __eq__(self, other):
        return self.notes == other.notes and self.auto_counter == other.auto_counter
    
    
    def add_note(self, text) -> Note:
        #create a note object, and add it to the list.
        print(f'Adding note: {text} Current Counter: {self.auto_counter}') 
        note = Note(self.auto_counter + 1, text) #notes are 1-indexed, while the auto_counter is 0-indexed.
        self.notes.append(note)
        self.auto_counter += 1
        print(f'Updated Counter: {self.auto_counter}')
        return note

    def remove_note(self, note):
        self.notes.remove(note)
        self.auto_counter -= 1
    
