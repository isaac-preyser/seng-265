import unittest
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()

    def test_login_logout(self):
        # Test logging out when already logged out
        with self.assertRaises(InvalidLogoutException):
            self.controller.logout()

        # Test logging in with incorrect username
        with self.assertRaises(InvalidLoginException):
            self.controller.login("wronguser", "clinic2024")

        # Test logging in with incorrect password
        with self.assertRaises(InvalidLoginException):
            self.controller.login("user", "wrongpassword")

        # Test logging in with correct credentials
        self.assertTrue(self.controller.login("user", "123456"), "Should be able to log in with correct credentials")

        # Test logging in when already logged in
        with self.assertRaises(DuplicateLoginException):
            self.controller.login("user", "123456")

        # Test logging out when logged in
        self.assertTrue(self.controller.logout(), "Should be able to log out when logged in")

        # Test logging in again after logging out
        self.assertTrue(self.controller.login("user", "123456"), "Should be able to log in again after logging out")

    def test_create_patient(self):
        # Test creating a patient when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        
        self.controller.login("user", "123456")

        # Test creating a patient
        patient = self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.assertIsNotNone(patient, "Patient should be created")
        self.assertEqual(patient.phn, "123", "Patient PHN should match")
        self.assertEqual(patient.name, "John Doe", "Patient name should match")

        # Test creating a patient with an existing PHN
        with self.assertRaises(IllegalOperationException):
            self.controller.create_patient("123", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")

    def test_list_patients(self):
        # Test listing patients when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.list_patients()
        
        self.controller.login("user", "123456")

        # Test listing patients when there are no patients
        patients = self.controller.list_patients()
        self.assertEqual(len(patients), 0, "There should be no patients")

        # Test listing patients after adding some patients
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.create_patient("124", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        patients = self.controller.list_patients()
        self.assertEqual(len(patients), 2, "There should be two patients")

    def test_delete_patient(self):
        # Test deleting a patient when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.delete_patient("123")

        # Test search_patient when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.search_patient("123")

        self.controller.login("user", "123456")

        # Test deleting a patient when there are no patients
        with self.assertRaises(IllegalOperationException):
            self.controller.delete_patient("123")

        # Test deleting a patient after adding some patients
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.create_patient("124", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        self.assertTrue(self.controller.delete_patient("123"), "Should be able to delete a patient")
        self.assertIsNone(self.controller.search_patient("123"), "Deleted patient should not be found")

        # Test deleting a patient that does not exist
        with self.assertRaises(IllegalOperationException):
            self.controller.delete_patient("999")

    def test_set_get_current_patient(self):
        # Test setting and getting the current patient when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.set_current_patient("123")
        with self.assertRaises(IllegalAccessException):
            self.controller.get_current_patient()

        # Test unsetting the current patient when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.unset_current_patient()

        self.controller.login("user", "123456")

        # Test setting and getting the current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        current_patient = self.controller.get_current_patient()
        self.assertIsNotNone(current_patient, "Current patient should be set")
        self.assertEqual(current_patient.phn, "123", "Current patient PHN should match")

        # Test unsetting the current patient
        self.controller.unset_current_patient()
        self.assertIsNone(self.controller.get_current_patient(), "Current patient should be unset") #return None by design, not an exception

    def test_create_note(self):
        self.controller.login("user", "123456")

        # Test creating a note when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.create_note("This is a test note.")

        # Test creating a note after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        note = self.controller.create_note("This is a test note.")
        self.assertIsNotNone(note, "Note should be created")
        self.assertEqual(note.text, "This is a test note.", "Note text should match")

    def test_update_patient(self):
        self.controller.login("user", "123456")

        # Test updating a patient when there are no patients
        with self.assertRaises(IllegalOperationException):
            self.controller.update_patient("123", "124", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")

        # Test updating a patient after adding some patients
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.create_patient("125", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        self.assertTrue(self.controller.update_patient("123", "124", "John Smith", "1990-01-01", "555-5555", "johnsmith@example.com", "123 Elm St"), "Should be able to update a patient")
        updated_patient = self.controller.search_patient("124")
        self.assertIsNotNone(updated_patient, "Updated patient should be found")
        self.assertEqual(updated_patient.name, "John Smith", "Updated patient name should match")
        self.assertEqual(updated_patient.email, "johnsmith@example.com", "Updated patient email should match")

        # Test updating a patient with a PHN that already exists
        with self.assertRaises(IllegalOperationException):
            self.controller.update_patient("124", "125", "John Smith", "1990-01-01", "555-5555", "johnsmith@example.com", "123 Elm St")

        # Test updating a patient that does not exist
        with self.assertRaises(IllegalOperationException):
            self.controller.update_patient("999", "998", "Nonexistent Patient", "2000-01-01", "555-5557", "nonexistent@example.com", "125 Elm St")

    def test_list_notes(self):
        self.controller.login("user", "123456")

        # Test listing notes when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.list_notes()

        # Test listing notes after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        self.controller.create_note("This is a test note.")
        notes = self.controller.list_notes()
        self.assertEqual(len(notes), 1, "There should be one note")
        self.assertEqual(notes[0].text, "This is a test note.", "Note text should match")

    def test_check_login(self):
        # Test check_login when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.check_login('some action')

        # Test check_login when logged in
        self.controller.login("user", "123456")
        self.assertTrue(self.controller.check_login('some action'), "Should be able to perform action when logged in")

    def test_search_note(self):
        # Test search_note when not logged in
        with self.assertRaises(IllegalAccessException):
            self.controller.search_note("001")

        self.controller.login("user", "123456")

        # Test searching for a note when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.search_note("001")

        # Test searching for a note after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        note = self.controller.create_note("This is a test note.")
        found_note = self.controller.search_note(note.code)
        self.assertIsNotNone(found_note, "Note should be found")
        self.assertEqual(found_note.text, "This is a test note.", "Note text should match")

        # Test searching for a note that does not exist, should return None
        self.assertIsNone(self.controller.search_note("999"), "Note should not be found")

    def test_update_note(self):
        self.controller.login("user", "123456")

        # Test updating a note when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.update_note("001", "Updated note text")

        # Test updating a note after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        note = self.controller.create_note("This is a test note.")
        self.assertTrue(self.controller.update_note(note.code, "Updated note text"), "Should be able to update the note")
        updated_note = self.controller.search_note(note.code)
        self.assertEqual(updated_note.text, "Updated note text", "Note text should be updated")

        # Test updating a note that does not exist
        self.assertFalse(self.controller.update_note("999", "Nonexistent note text"), "Should not be able to update a note that does not exist")

    def test_delete_note(self):
        self.controller.login("user", "123456")

        # Test deleting a note when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.delete_note("001")

        # Test deleting a note after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        note = self.controller.create_note("This is a test note.")
        self.assertTrue(self.controller.delete_note(note.code), "Should be able to delete the note")
        self.assertIsNone(self.controller.search_note(note.code), "Deleted note should not be found")

        # Test deleting a note that does not exist
        self.assertFalse(self.controller.delete_note("999"), "Should not be able to delete a note that does not exist")

    def test_retrieve_notes(self):
        self.controller.login("user", "123456")

        # Test retrieving notes when there is no current patient
        with self.assertRaises(NoCurrentPatientException):
            self.controller.retrieve_notes("test")

        # Test retrieving notes after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        self.controller.create_note("This is a test note.")
        self.controller.create_note("Another test note.")
        notes = self.controller.retrieve_notes("test")
        self.assertEqual(len(notes), 2, "There should be two notes containing 'test'")
        self.assertIn("This is a test note.", [note.text for note in notes], "Note text should match")
        self.assertIn("Another test note.", [note.text for note in notes], "Note text should match")

        # Test retrieving notes with a search term that does not match any notes
        notes = self.controller.retrieve_notes("nonexistent")
        self.assertEqual(len(notes), 0, "There should be no notes containing 'nonexistent'")

if __name__ == '__main__':
    unittest.main()