from clinic.note import Note
from clinic.patient import Patient
#new functionality: exception handling
from clinic import exception 

class Controller: 
    def __init__(self, autosave = False):
        self.locked = True
        self.patients = []
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
    
    #create a patient with the supplied information.
    def create_patient(self, phn, name, birth_date, phone, email, address) -> Patient:
        self.check_login('create a patient')
        #make a new patient object
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        for patient in self.patients:
            if patient.phn == new_patient.phn:
                print('Patient already exists.')
                raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient already exists.')
        self.patients.append(new_patient)
        print(f'Patient created: {new_patient.name} - {new_patient.phn}')
        return new_patient
    
    def search_patient(self, phn):
        self.check_login('search for a patient')
        for patient in self.patients:
            if patient.phn == phn:
                print(f'Patient found: {patient.name} - {patient.phn}')
                return patient
        print('Patient not found.')
        return None
    
    #this function returns a list of patients that have names that contain the supplied substring (search_term)
    def retrieve_patients(self, search_term) -> list[Patient]:
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
            raise exception.no_current_patient_exception.NoCurrentPatientException('No patients to update.')
        #if the current patient is the one being updated, we cannot update.
        #(if we have a current_patient, and the PHN is the same, we cannot update)
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot update the current patient.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - cannot update the current patient. (unset the current patient first)')

        #now we can search for patient with the supplied PHN.
        patient_to_update = None
        for patient in self.patients:
            if patient.phn == phn:
                patient_to_update = patient
                break
        #if the patient is not found, we cannot update.
        if not patient_to_update:
            print('Patient not found.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient not found.')

        #check if the new PHN is already in use by another patient.
        for patient in self.patients:
            if patient.phn == new_phn and patient.phn != phn:
                print('Patient with new PHN already exists. Cannot update.')
                raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - new PHN already in use.')
        
        patient_to_update.update(new_phn, name, birth_date, phone, email, address)
        print('Patient updated.')
        return True
    
    #list all patients in the controller.    
    def list_patients(self) -> list[Patient]:
        self.check_login('list patients')
        return self.patients #returns a list of patients.
    
    #delete a patient with the supplied PHN.
    def delete_patient(self, phn) -> bool:
        self.check_login('delete a patient')
        if not self.patients:
            #if there are no patients, there is nothing to delete.
            print('No patients to delete.')
            return False
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot delete the current patient.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - cannot delete the current patient.')
        for patient in self.patients:
            if patient.phn == phn:
                self.patients.remove(patient)
                print('Patient deleted.')
                return True
        print('Patient not found.')
        raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient not found.')
    
    #get the current patient.
    def get_current_patient(self) -> Patient:
        self.check_login('get the current patient')
        return self.current_patient
    
    #set the current patient to the patient with the supplied PHN.
    def set_current_patient(self, phn) -> bool:
        self.check_login('set the current patient')
            
        # check if the patient exists in the list of patients (this is done via PHN).
        for patient in self.patients:
            if patient.phn == phn:
                self.current_patient = patient
                print(f'Current patient set to {self.current_patient.name}.')
                return True
        print('Patient not found.')
        raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient not found.')

    
    #unset the current patient.
    def unset_current_patient(self) -> bool:
        self.check_login('unset the current patient')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - no current patient set.')
        self.current_patient = None
        return True
    
    #create a note for the current patient.
    def create_note(self, text) -> Note:
        self.check_login('create a note')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return None
        #create a note and add it to the patient (via patient -> patient record)
        note = self.current_patient.add_note(text)
        return note
    
    #This function searches for a note (under the current patient) by it's code. (each note should have a unique code.)
    def search_note(self, code) -> Note:
        self.check_login('search for a note')
        if not self.current_patient:
            print('No current patient set, set a current patient before searching for a note.')  
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return None
        note = self.current_patient.get_note(code)
        if note:
            print(f'Note found: "{note.text}" Time: {note.timestamp}')
            return note
        print('Note not found.')
        raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - note not found.')
        return None
    

    # This function searches for a note (under the current patient) by its code. (each note should have a unique code.)
    def search_note(self, code) -> Note:
        self.check_login('search for a note')
        if not self.current_patient:
            print('No current patient set, set a current patient before searching for a note.')  
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return None
        note = self.current_patient.get_note(code)
        if note:
            print(f'Note found: "{note.text}" Time: {note.timestamp}')
            return note
        print('Note not found.')
        return None

    # If one of the patient's notes contains the supplied substring, add it to the results list, and return it.
    def retrieve_notes(self, search_term) -> list[Note]:
        self.check_login('retrieve notes')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return None
        return self.current_patient.retrieve_notes(search_term)
    
    # Updates a note with a supplied code, and a new text.
    def update_note(self, code, text) -> bool:
        self.check_login('update a note')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return False
        # Update the note via the patient.
        if self.current_patient.update_note(code, text):
            print('Note updated.')
            return True
        print('Note not found.')
        return False
    
    # Removes a note with a supplied code.
    def delete_note(self, code) -> bool:
        self.check_login('delete a note')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return False  
        return self.current_patient.delete_note(code) 
    
    # Lists notes for the current patient.
    def list_notes(self) -> list[Note]:
        self.check_login('list notes')
        if not self.current_patient:
            print('No current patient set.')
            raise exception.no_current_patient_exception.NoCurrentPatientException('No current patient set.')
            return None
        print("Listing notes:")
        return self.current_patient.list_notes()
