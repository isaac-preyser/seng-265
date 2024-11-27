from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
import pickle

class NoteDAOPickle(NoteDAO):
    def __eq__(self, other):
        if not isinstance(other, NoteDAOPickle):
            return False
        return self.notes == other.notes
    

    def __init__(self, phn=None, patient_record=None):
        self.notes = {}
        self.phn = phn #needed for loading/storing note files. 
        self.patient_record = patient_record
        #load notes from file.
        self.load_notes()



    def load_notes(self) -> int:
        #each record file will be named after the patient's PHN.
        #e.g. 1234567890.dat, which is found at clinic/records/1234567890.dat
        #this means we need access to the patient's PHN (therefore we must pass it in)

        #this function will return an integer representing the number of notes loaded.

        #this function should be called after the patient_dao has loaded the patient's record.
        try:
            with open(f'clinic/records/{self.phn}.dat', 'rb') as file:
                self.notes = pickle.load(file)
                # print(f'Loaded {len(self.notes)} notes.')
                number_of_notes = len(self.notes)
        except FileNotFoundError:
            self.notes = {}
            # print('No notes found.')
            number_of_notes = 0
        
        #set the auto_counter to the number of notes loaded.
        
        return number_of_notes



    def save_notes(self):
        #each record file will be named after the patient's PHN.
        #e.g. 1234567890.dat, which is found at clinic/records/1234567890.dat
        #this means we need access to the patient's PHN (therefore we must pass it in)

        #this function should be called after the patient_dao has saved the patient's record.
        with open(f'clinic/records/{self.phn}.dat', 'wb') as file:
            pickle.dump(self.notes, file)
            # print(f'Wrote {len(self.notes)} notes to file.')

    
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
        #save the notes to file.
        self.save_notes()
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
            #save the notes to file.
            self.save_notes()
            return True
        return False
    
    def delete_note(self, code):
        if code in self.notes:
            del self.notes[code]
            #save the notes to file.
            self.save_notes()
            return True
        return False
    
    def list_notes(self):
        return list(self.notes.values())    
    