import unittest
from clinic.patient_record import PatientRecord
from clinic.note import Note

class TestPatientRecord(unittest.TestCase):
    def setUp(self):
        self.record = PatientRecord()

    def test_add_note_increases_counter(self):
        note = self.record.add_note("First note")
        self.assertEqual(self.record.auto_counter, 1)

    def test_add_note_appends_to_notes(self):
        note = self.record.add_note("First note")
        self.assertIn(note, self.record.notes)

    def test_remove_note_decreases_counter(self):
        note1 = self.record.add_note("First note")
        note2 = self.record.add_note("Second note")
        self.record.remove_note(note1)
        self.assertEqual(self.record.auto_counter, 1)
        self.assertNotIn(note1, self.record.notes)

    def test_remove_note_removes_from_notes(self):
        note = self.record.add_note("First note")
        self.record.remove_note(note)
        self.assertNotIn(note, self.record.notes)

    def test_equality(self):
        record1 = PatientRecord()
        record2 = PatientRecord()
        self.assertEqual(record1, record2)
        record1.add_note("First note")
        self.assertNotEqual(record1, record2)
        record2.add_note("First note")
        self.assertEqual(record1, record2)

if __name__ == '__main__':
    unittest.main()