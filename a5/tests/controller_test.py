import os
import unittest
from clinic import exception
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()
        self.controller.load_users()
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
    
    def test_login_success(self):
        result = self.controller.login("user", "123456")
        self.assertTrue(result)
        self.assertEqual(self.controller.current_user, "user")
        self.assertFalse(self.controller.locked)

    def test_login_invalid_password(self):
        with self.assertRaises(InvalidLoginException):
            self.controller.login("user", "wrongpassword")

    def test_login_invalid_user(self):
        with self.assertRaises(InvalidLoginException):
            self.controller.login("nonexistent_user", "123456")

    def test_duplicate_login(self):
        self.controller.login("user", "123456")
        with self.assertRaises(DuplicateLoginException):
            self.controller.login("user", "123456")

    def test_logout_success(self):
        self.controller.login("user", "123456")
        result = self.controller.logout()
        self.assertTrue(result)
        self.assertIsNone(self.controller.current_user)
        self.assertTrue(self.controller.locked)

    def test_logout_when_already_logged_out(self):
        with self.assertRaises(InvalidLogoutException):
            self.controller.logout()

    def test_create_patient_success(self):
        self.controller.login("user", "123456")
        patient = self.controller.create_patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, "John Doe")

    def test_create_patient_without_login(self):
        with self.assertRaises(exception.illegal_access_exception.IllegalAccessException):
            self.controller.create_patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")

    def test_search_patient_found(self):
        self.controller.login("user", "123456")
        self.controller.create_patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        patient = self.controller.search_patient("123456789")
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, "John Doe")

    def test_search_patient_not_found(self):
        self.controller.login("user", "123456")
        patient = self.controller.search_patient("987654321")
        self.assertIsNone(patient)




if __name__ == '__main__':
    unittest.main()