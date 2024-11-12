#new functionality: exception handling
from clinic import exception 
from clinic.dao.patient_dao_json import PatientDAOJSON


class Controller: 
    def __init__(self, autosave = False):
        self.locked = True
        self.patients = PatientDAOJSON() #list of patients in the controller.
        #user/password for login. consider changing the init function to take arguments to do a constructor here. 
        #NEW FUNCTIONALITY: multiple users. 
        self.users = {'user': '123456', 'ali': '@G00dPassw0rd'}
        self.current_user = None
        self.current_patient = None #this is used to store the patient that is currently being worked on.
        #NEW FUNCTIONALITY: autosave
        self.autosave = autosave    

    def logout(self) -> bool:
        if self.locked:
            print('You are already logged out.') #not sure if this is necessary
            raise exception.invalid_logout_exception.InvalidLogoutException('Invalid logout.')
        self.locked = True
        print('You have been logged out.')
        return True
    
    def login(self, user, password) -> bool:
        if not self.locked:
            print('You are already logged in.')
            raise exception.duplicate_login_exception.DuplicateLoginException('Duplicate login.')
        if user in self.users and self.users[user] == password:
            self.locked = False
            self.current_user = user 
            print('You have been logged in.')
            return True
        print('Invalid password.')
        raise exception.invalid_login_exception.InvalidLoginException('Invalid login - invalid password or username.')
    
    #generic function to check if the controller is locked.
    def check_login(self, action) -> bool:
        if self.locked:
            print(f'You must be logged in to {action}.')
            raise exception.illegal_access_exception.IllegalAccessException(f'Illegal access. - {action}')
        return True
    
    def check_has_current_patient(self, action) -> bool:
        if not self.current_patient:
            print(f'You must set a current patient to {action}.')
            raise exception.no_current_patient_exception.NoCurrentPatientException(f'No current patient set. - {action}')
        return True
    
    #create a patient with the supplied information.
    def create_patient(self, phn, name, birth_date, phone, email, address):
        self.check_login('create a patient')
        #make a new patient object via the DAO
        self.patients.create_patient(phn, name, birth_date, phone, email, address)
        return self.patients.get_patient(phn)
        
    
    def search_patient(self, phn):
        self.check_login('search for a patient')
        for patient in self.patients:
            if patient.phn == phn:
                print(f'Patient found: {patient.name} - {patient.phn}')
                return patient
        print('Patient not found.')
        return None
    
    #this function returns a list of patients that have names that contain the supplied substring (search_term)
    def retrieve_patients(self, search_term):
        self.check_login('retrieve patients')
        results = []
        for patient in self.patients:
            if search_term in patient.name:
                results.append(patient)
        print(f'{len(results)} patients found.')
        return results

    #update a patient's information, given an existing PHN and new user information. 
    def update_patient(self, phn, new_phn, name, birth_date, phone, email, address) -> bool:
        #cannot update a patient if the controller is locked.
        self.check_login('update a patient')
        #if there are no patients, there is nothing to update.
        if not self.patients:
            print('No patients to update.')
            raise exception.illegal_operation_exception.IllegalOperationException('No patients to update.')
        #if the current patient is the one being updated, we cannot update.
        #(if we have a current_patient, and the PHN is the same, we cannot update)
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot update the current patient.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - cannot update the current patient. (unset the current patient first)')
        #update the patient via the DAO.
        self.patients.update_patient(phn, new_phn, name, birth_date, phone, email, address)
        return True
    
    #list all patients in the controller.    
    def list_patients(self):
        self.check_login('list patients')
        return self.patients.list_patients()
    
    #delete a patient with the supplied PHN.
    def delete_patient(self, phn) -> bool:
        self.check_login('delete a patient')
        if not self.patients:
            print('No patients to delete.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - No patients to delete.')
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot delete the current patient.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - cannot delete the current patient.')
        #immediately delegate to the DAO. 
        return self.patients.delete_patient(phn)
    

    #get the current patient.
    def get_current_patient(self):
        self.check_login('get the current patient')
        #intentionally returning None if there is no current patient, do not throw an exception.
        return self.current_patient
    
    #set the current patient to the patient with the supplied PHN.
    def set_current_patient(self, phn) -> bool:
        self.check_login('set the current patient')
        patient = self.search_patient(phn)
        if patient:
            self.current_patient = patient
            return True
        print('Patient not found.')
        raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient not found.')

    
    #unset the current patient.
    def unset_current_patient(self) -> bool:
        self.check_login('unset the current patient')
        self.current_patient = None
        return True
    
    #create a note for the current patient.
    def create_note(self, text):
        self.check_login('create a note')
        self.check_has_current_patient('create a note')
        #create a note and add it to the patient (via patient -> patient record)
        note = self.current_patient.add_note(text)
        return note
    
    #This function searches for a note (under the current patient) by it's code. (each note should have a unique code.)
    def search_note(self, code):
        self.check_login('search for a note')
        self.check_has_current_patient('search for a note')
        note = self.current_patient.get_note(code)
        if note:
            print(f'Note found: "{note.text}" Time: {note.timestamp}')
            return note
        print(f'Note (with code {code}) not found.')
        return None #intentional, do not throw an exception.
    

    # If one of the patient's notes contains the supplied substring, add it to the results list, and return it.
    def retrieve_notes(self, search_term):
        self.check_login('retrieve notes')
        self.check_has_current_patient('retrieve notes')
        return self.current_patient.retrieve_notes(search_term)
    
    # Updates a note with a supplied code, and a new text.
    def update_note(self, code, text) -> bool:
        self.check_login('update a note')
        self.check_has_current_patient('update a note')
        # Update the note via the patient.
        if self.current_patient.update_note(code, text):
            print('Note updated.')
            return True
        print('Note not found.')
        return False
    
    # Removes a note with a supplied code.
    def delete_note(self, code) -> bool:
        self.check_login('delete a note')
        self.check_has_current_patient('delete a note') 
        return self.current_patient.delete_note(code) 
    
    # Lists notes for the current patient.
    def list_notes(self):
        self.check_login('list notes')
        self.check_has_current_patient('list notes')
        print("Listing notes:")
        return self.current_patient.list_notes()
