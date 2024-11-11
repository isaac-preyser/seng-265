import unittest
from clinic.patient_record import PatientRecord
from clinic.note import Note

class TestPatientRecord(unittest.TestCase):
    def setUp(self):
        self.record = PatientRecord()

    def test_add_note(self):
        note = self.record.add_note("First note")
        self.assertEqual(note.text, "First note")
        self.assertEqual(note.code, 1)
        self.assertEqual(len(self.record.notes), 1)

    def test_remove_note_success(self):
        self.record.add_note("First note")
        self.assertTrue(self.record.remove_note(1))
        self.assertEqual(len(self.record.notes), 0)

    def test_remove_note_failure(self):
        self.record.add_note("First note")
        self.assertFalse(self.record.remove_note(2))
        self.assertEqual(len(self.record.notes), 1)

    def test_update_note_success(self):
        self.record.add_note("First note")
        self.assertTrue(self.record.update_note(1, "Updated note"))
        self.assertEqual(self.record.notes[0].text, "Updated note")

    def test_update_note_failure(self):
        self.record.add_note("First note")
        self.assertFalse(self.record.update_note(2, "Updated note"))
        self.assertEqual(self.record.notes[0].text, "First note")

    def test_list_notes(self):
        self.record.add_note("First note")
        self.record.add_note("Second note")
        notes = self.record.list_notes()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, "Second note")
        self.assertEqual(notes[1].text, "First note")

    def test_equality(self):
        record1 = PatientRecord()
        record2 = PatientRecord()
        record1.add_note("First note")
        record2.add_note("First note")
        self.assertEqual(record1, record2)
        
    def test_str(self):
        self.record.add_note("First note")
        self.assertEqual(str(self.record), 'Patient Record: [Note 1, text: "First note"]')

if __name__ == '__main__':
    unittest.main()