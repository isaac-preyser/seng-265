from clinic.dao.note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __eq__(self, other):
        if not isinstance(other, NoteDAOPickle):
            return False
        return self.notes == other.notes
    def __init__(self):
        self.notes = []

    def __getitem__(self, index):
        return self.notes[index]

    def __iter__(self):
        return iter(self.notes)
    
    def __len__(self):
        return len(self.notes)
    
    def search_note(self, code):
        for note in self.notes:
            if note.code == code:
                return note
        return None
    
    def create_note(self, text):
        note = Note.create(text)
        self.notes.append(note)
        return note
    
    def retrieve_notes(self, search_string):
        results = []
        for note in self.notes:
            if search_string in note.text:
                results.append(note)
        return results
    
    def update_note(self, code, text):
        for i, note in enumerate(self.notes):
            if note.code == code:
                self.notes[i] = note.update(text)
                return True
        return False
    
    def delete_note(self, code):
        self.notes = [note for note in self.notes if note.code != code]
        return True
    
    def list_notes(self):
        return self.notes
    