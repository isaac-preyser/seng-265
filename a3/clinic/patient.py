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
    
    def search_notes(self, search_term):
        results = []
        for note in self.record.notes:
            if search_term in note.text:
                results.append(note)
        return results