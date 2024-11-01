from clinic.note import Note

class PatientRecord:
    def __init__(self):
        self.notes = [] #contains a list of notes. 
        self.auto_counter = 0 #counts number of notes in the record. 

    def __eq__(self, other):
        return self.notes == other.notes and self.auto_counter == other.auto_counter

    def __str__(self):
        return f'Patient Record: {self.notes}'    
    
    def add_note(self, text) -> Note:
        #create a note object, and add it to the list.
        print(f'Adding note: {text} Current Counter: {self.auto_counter}') 
        note = Note(self.auto_counter + 1, text) #notes are 1-indexed, while the auto_counter is 0-indexed.
        self.notes.append(note)
        self.auto_counter += 1
        print(f'Updated Counter: {self.auto_counter}')
        return note

    #given a code, find and remove a note. 
    def remove_note(self, code):
        for note in self.notes:
            if note.code == code:
                self.notes.remove(note)
                print(f'Removed {note.code}')
                self.auto_counter -= 1
                return True
        return False

    def update_note(self, code, text):
        for note in self.notes:
            if note.code == code:
                note.update(text)
                return True
        return False 
    
