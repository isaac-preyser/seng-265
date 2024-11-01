import unittest
from clinic.controller import Controller
from clinic.patient import Patient

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()

    def test_login_logout(self):
        # Test logging out when already logged out
        self.assertFalse(self.controller.logout(), "Should not be able to log out when already logged out")

        # Test logging in with incorrect username
        self.assertFalse(self.controller.login("wronguser", "clinic2024"), "Should not be able to log in with incorrect username")

        # Test logging in with incorrect password
        self.assertFalse(self.controller.login("user", "wrongpassword"), "Should not be able to log in with incorrect password")

        # Test logging in with correct credentials
        self.assertTrue(self.controller.login("user", "clinic2024"), "Should be able to log in with correct credentials")

        # Test logging in when already logged in
        self.assertFalse(self.controller.login("user", "clinic2024"), "Should not be able to log in when already logged in")

        # Test logging out when logged in
        self.assertTrue(self.controller.logout(), "Should be able to log out when logged in")

        # Test logging in again after logging out
        self.assertTrue(self.controller.login("user", "clinic2024"), "Should be able to log in again after logging out")

    def test_create_patient(self):
        self.controller.login("user", "clinic2024")

        # Test creating a patient
        patient = self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.assertIsNotNone(patient, "Patient should be created")
        self.assertEqual(patient.phn, "123", "Patient PHN should match")
        self.assertEqual(patient.name, "John Doe", "Patient name should match")

        # Test creating a patient with an existing PHN
        patient = self.controller.create_patient("123", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        self.assertIsNone(patient, "Should not be able to create a patient with an existing PHN")

    def test_list_patients(self):
        self.controller.login("user", "clinic2024")

        # Test listing patients when there are no patients
        patients = self.controller.list_patients()
        self.assertEqual(len(patients), 0, "There should be no patients")

        # Test listing patients after adding some patients
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.create_patient("124", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        patients = self.controller.list_patients()
        self.assertEqual(len(patients), 2, "There should be two patients")

    def test_delete_patient(self):
        self.controller.login("user", "clinic2024")

        # Test deleting a patient when there are no patients
        self.assertFalse(self.controller.delete_patient("123"), "Should not be able to delete a patient when there are no patients")

        # Test deleting a patient after adding some patients
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.create_patient("124", "Jane Doe", "1991-01-01", "555-5556", "jane@example.com", "124 Elm St")
        self.assertTrue(self.controller.delete_patient("123"), "Should be able to delete a patient")
        self.assertIsNone(self.controller.search_patient("123"), "Deleted patient should not be found")

    def test_set_get_current_patient(self):
        self.controller.login("user", "clinic2024")

        # Test setting and getting the current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        current_patient = self.controller.get_current_patient()
        self.assertIsNotNone(current_patient, "Current patient should be set")
        self.assertEqual(current_patient.phn, "123", "Current patient PHN should match")

    def test_create_note(self):
        self.controller.login("user", "clinic2024")

        # Test creating a note when there is no current patient
        self.assertIsNone(self.controller.create_note("This is a test note."), "Should not be able to create a note when there is no current patient")

        # Test creating a note after setting a current patient
        self.controller.create_patient("123", "John Doe", "1990-01-01", "555-5555", "john@example.com", "123 Elm St")
        self.controller.set_current_patient("123")
        note = self.controller.create_note("This is a test note.")
        self.assertIsNotNone(note, "Note should be created")
        self.assertEqual(note.text, "This is a test note.", "Note text should match")

if __name__ == '__main__':
    unittest.main()