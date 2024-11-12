from clinic.dao.note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __eq__(self, other):
        if not isinstance(other, NoteDAOPickle):
            return False
        return self.notes == other.notes
    def __init__(self):
        self.notes = {}

    
    #allow "list" functionality for the notes object.
    def __iter__(self):
        return iter(self.notes.values())
    
    def __len__(self):
        return len(self.notes)
    
    def search_note(self, code):
        if code in self.notes:
            return self.notes[code]
        return None
    
    def create_note(self, code, text):
        note = Note.create(code, text)
        self.notes[code] = note
        return note
    
    def retrieve_notes(self, search_string):
        results = []
        for note in self.notes.values():
            if search_string in note.text:
                results.append(note)
        return results
    
    def update_note(self, code, text):
        if code in self.notes:
            self.notes[code].update(text)
            return True
        return False
    
    def delete_note(self, code):
        if code in self.notes:
            del self.notes[code]
            return True
        return False
    
    def list_notes(self):
        return list(self.notes.values())    
    