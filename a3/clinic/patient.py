from clinic.note import Note
from clinic.patient_record import PatientRecord


class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord()

    def __eq__(self, other):
        return self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date and self.phone == other.phone and self.email == other.email and self.address == other.address and self.record == other.record
    
    def retrieve_notes(self, search_term) -> list[Note]:
        results = []
        for note in self.record.notes:
            if search_term in note.text:
                results.append(note)
        return results
    
    def get_note(self, code) -> Note:
        for note in self.record.notes:
            if note.code == code:
                return note
        return None

    #update a note in the patient's record.
    def update_note(self, code, text) -> bool:
        return self.record.update_note(code, text)
    
    #update self. 
    def update(self, phn, name, birth_date, phone, email, address):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        return self
    
    def add_note(self, text) -> Note:
        return self.record.add_note(text)
    
    def delete_note(self, code) -> bool: 
        return self.record.remove_note(code)    
    
    def list_notes(self) -> list[Note]:
        return self.record.list_notes()
    