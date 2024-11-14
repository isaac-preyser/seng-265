import os
from unittest import TestCase
from unittest import main
import unittest
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class TestPatientRecord(TestCase):

    def setUp(self):
        # set autosave to False to avoid testing persistence
        # self.controller = Controller(autosave=False)

        # set autosave to True to test persistence
        self.record = PatientRecord()

    # comment the tearDown method to see the file when the test ends.
    def tearDown(self):
        patients_file = 'clinic/patients.json'
        patients_file_exists = os.path.exists(patients_file)
        records_path = 'clinic/records'
        if os.path.exists(records_path):
            filenames = os.listdir(records_path)
            for filename in filenames:
                record_file_path = os.path.join(records_path, filename)
                if os.path.isfile(record_file_path):
                    os.remove(record_file_path)
        # removing the patients file later to avoid concurrency issues
        if patients_file_exists:
            os.remove(patients_file)

    def reset_persistence(self):
        # reset persistence will be ignored if autosave is False
        # otherwise it will reinstantiate the controller and reload every file
        if self.controller.autosave:
            self.controller = Controller(autosave=True)
            self.controller.login("user", "123456")       


    def test_add_note(self):
        note = self.record.add_note("First note")
        self.assertEqual(note.text, "First note")
        self.assertEqual(note.code, 1)
        self.assertEqual(len(self.record.noteDAO), 1)

    def test_remove_note_success(self):
        self.record.add_note("First note")
        self.assertTrue(self.record.remove_note(1))
        self.assertEqual(len(self.record.noteDAO), 0)

    def test_remove_note_failure(self):
        self.record.add_note("First note")
        self.assertFalse(self.record.remove_note(2))
        self.assertEqual(len(self.record.noteDAO), 1)

    def test_update_note_success(self):
        self.record.add_note("First note")
        self.assertTrue(self.record.update_note(1, "Updated note"))
        self.assertEqual(self.record.noteDAO.search_note(1).text, "Updated note")

    def test_update_note_failure(self):
        self.record.add_note("First note")
        self.assertFalse(self.record.update_note(2, "Updated note"))
        self.assertEqual(self.record.noteDAO.search_note(1).text, "First note")
    
    
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