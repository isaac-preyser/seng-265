from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self):
        self.notes = NoteDAOPickle() #list of notes in the record. 
        self.auto_counter = 0 #counts number of notes in the record. 

    def __eq__(self, other):
        return self.notes == other.notes and self.auto_counter == other.auto_counter

    def __str__(self):
        output = 'Patient Record: ['
        for note in self.notes:
            output += f'Note {note.code}, text: "{note.text}"'
        output += ']'
        return output   
    
    #given a code, find and return a note.
    def add_note(self, text):
        #create a note object, and add it to the list.
        note = self.notes.create_note(self.auto_counter + 1, text)
        self.auto_counter += 1
        return note
    
    #given a code, find and remove a note. 
    def remove_note(self, code) -> bool:
        for note in self.notes:
            if note.code == code:
                self.notes.delete_note(note.code)
                #print(f'Removed {note.code}')
                self.auto_counter -= 1
                return True
        return False

    #update a note given a code and new text. (delegate to the note object)
    def update_note(self, code, text) -> bool:
        return self.notes.update_note(code, text)
    
    # sort notes by timestamp and list them.
    def list_notes(self):
        #sort the notes by timestamp (recent first) and return them. Not sure if I can use dict.values() here.
        sorted_notes = sorted(self.notes, key=lambda x: x.timestamp, reverse=True) #sort by timestamp, most recent first (via lambda function)
        for note in sorted_notes:
            print(f'Note {note.code}: "{note.text}" Time: {note.timestamp}')
        return sorted_notes
    
    #search for a note with a given search term.
    def retrieve_notes(self, search_term):
        return self.notes.retrieve_notes(search_term)
    
