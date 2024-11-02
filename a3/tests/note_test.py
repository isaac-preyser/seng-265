import unittest
from datetime import datetime, timedelta
from clinic.note import Note

class TestNote(unittest.TestCase):
    def test_note_equality_same_code_text_and_timestamp(self):
        note1 = Note("001", "Test note")
        note2 = Note("001", "Test note")
        self.assertTrue(note1 == note2)

    def test_note_equality_different_code(self):
        note1 = Note("001", "Test note")
        note2 = Note("002", "Test note")
        self.assertFalse(note1 == note2)

    def test_note_equality_different_text(self):
        note1 = Note("001", "Test note")
        note2 = Note("001", "Different text")
        self.assertFalse(note1 == note2)

    def test_note_equality_different_timestamp(self):
        note1 = Note("001", "Test note")
        note2 = Note("001", "Test note")
        note2.timestamp = note1.timestamp + timedelta(seconds=11)
        self.assertFalse(note1 == note2)

    def test_note_equality_within_time_difference(self):
        note1 = Note("001", "Test note")
        note2 = Note("001", "Test note")
        note2.timestamp = note1.timestamp + timedelta(seconds=5)
        self.assertTrue(note1 == note2)

    def test_note_str(self):
        note = Note("001", "Test note")
        expected_str = f'{note.code} - {note.text} : {note.timestamp}'
        self.assertEqual(str(note), expected_str)

    def test_note_update(self):
        note = Note("001", "Test note")
        old_timestamp = note.timestamp
        note.update("Updated note")
        self.assertEqual(note.text, "Updated note")
        self.assertNotEqual(note.timestamp, old_timestamp)

    def test_note_update_code_unchanged(self):
        note = Note("001", "Test note")
        note.update("Updated note")
        self.assertEqual(note.code, "001")

if __name__ == '__main__':
    unittest.main()