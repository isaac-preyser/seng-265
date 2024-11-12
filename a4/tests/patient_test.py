import unittest
from clinic.patient import Patient
from clinic.note import Note
from clinic.patient_record import PatientRecord

class TestPatient(unittest.TestCase):
    def setUp(self):
        self.patient = Patient(
            phn="123456789",
            name="John Doe",
            birth_date="1990-01-01",
            phone="555-1234",
            email="john.doe@example.com",
            address="123 Main St"
        )
        self.patient.record.add_note = lambda text: Note(
            code="001", text=text
        )
        self.patient.record.update_note = lambda code, text: Note(
            code=code, text=text
        )
        self.patient.record.remove_note = lambda code: True
        self.patient.record.notes.notes = {
            "001": Note(code="001", text="First note"),
            "002": Note(code="002", text="Second note")
        }

    def test_update_patient_info(self):
        self.patient.update(
            phn="987654321",
            name="Jane Doe",
            birth_date="1985-05-05",
            phone="555-5678",
            email="jane.doe@example.com",
            address="456 Elm St"
        )
        self.assertEqual(self.patient.phn, "987654321")
        self.assertEqual(self.patient.name, "Jane Doe")
        self.assertEqual(self.patient.birth_date, "1985-05-05")
        self.assertEqual(self.patient.phone, "555-5678")
        self.assertEqual(self.patient.email, "jane.doe@example.com")
        self.assertEqual(self.patient.address, "456 Elm St")

    def test_add_note_to_patient_record(self):
        note = self.patient.add_note(
            text="This is a new note"
        )
        self.assertEqual(note.text, "This is a new note")

    def test_retrieve_notes_from_patient_record(self):
        notes = self.patient.retrieve_notes(
            search_term="First"
        )
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, "First note")

    def test_get_note_by_code(self):
        note = self.patient.get_note(
            code="001"
        )
        self.assertIsNotNone(note)
        self.assertEqual(note.code, "001")
        self.assertEqual(note.text, "First note")

    def test_update_note_in_patient_record(self):
        note = self.patient.update_note(
            code="001",
            text="Updated note"
        )
        self.assertEqual(note.text, "Updated note")

    def test_delete_note_from_patient_record(self):
        result = self.patient.delete_note(
            code="001"
        )
        self.assertTrue(result)

    def test_list_all_notes(self):
        notes = self.patient.list_notes()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, "Second note") #most recent note first
        self.assertEqual(notes[1].text, "First note")



if __name__ == '__main__':
    unittest.main()