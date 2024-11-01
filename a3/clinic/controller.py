from clinic.patient import Patient

class Controller: 
    def __init__(self):
        self.locked = True
        self.patients = []
        #user/password for login. consider changing the init function to take arguments to do a constructor here. 
        self.password = 'clinic2024' #default password  
        self.user = 'user' #default user
        self.current_patient = None #this is used to store the patient that is currently being worked on.

    def logout(self):
        if self.locked:
            print('You are already logged out.') #not sure if this is necessary
            return False
        self.locked = True
        print('You have been logged out.')
        return True
    
    def login(self, user, password):
        if not self.locked:
            print('You are already logged in.')
            return False
        if password == self.password and user == self.user:
            self.locked = False
            print('You have been logged in.')
            return True
        print('Invalid password.')
        return False
    
    def check_login(self, action):
        if self.locked:
            print(f'You must be logged in to {action}.')
            return False
        return True
    
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if not self.check_login('create a patient'):
            return None
        #make a new patient object
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        for patient in self.patients:
            if patient.phn == new_patient.phn:
                print('Patient already exists.')
                return None #this nehavior might not be desirable.
        self.patients.append(new_patient)
        print(f'Patient created: {new_patient.name} - {new_patient.phn}')
        return new_patient
    
    def search_patient(self, phn):
        if not self.check_login('search for a patient'):
            return None
        for patient in self.patients:
            if patient.phn == phn:
                print(f'Patient found: {patient.name} - {patient.phn}')
                return patient
        print('Patient not found.')
        return None
    
    #this function returns a list of patients that have names that contain the supplied substring (search_term)
    def retrieve_patients(self, search_term):
        if not self.check_login('retrieve patients'):
            return None
        results = []
        for patient in self.patients:
            if search_term in patient.name:
                results.append(patient)
        print(f'{len(results)} patients found.')
        return results

    #update a patient's information, given an existing PHN and new user information. 
    def update_patient(self, phn, new_phn, name, birth_date, phone, email, address):
        #cannot update a patient if the controller is locked.
        if not self.check_login('update a patient'):
            return False
        #if there are no patients, there is nothing to update.
        if not self.patients:
            print('No patients to update.')
            return False
        #if the current patient is the one being updated, we cannot update.
        #(if we have a current_patient, and the PHN is the same, we cannot update)
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot update the current patient.')
            return False

        #now we can search for patient with the supplied PHN.
        patient_to_update = None
        for patient in self.patients:
            if patient.phn == phn:
                patient_to_update = patient
                break
        #if the patient is not found, we cannot update.
        if not patient_to_update:
            print('Patient not found.')
            return False

        #check if the new PHN is already in use by another patient.
        for patient in self.patients:
            if patient.phn == new_phn and patient.phn != phn:
                print('Patient with new PHN already exists. Cannot update.')
                return False
        
        patient_to_update.update(new_phn, name, birth_date, phone, email, address)
        print('Patient updated.')
        return True
    
        
    def list_patients(self):
        if not self.check_login('list patients'):
            return None
        #print('Patients:')
        # for patient in self.patients:
        #     print(patient.name)
        return self.patients #returns a list of patients.
    
    def delete_patient(self, phn):
        if not self.check_login('delete a patient'):
            return False
        if not self.patients:
            #if there are no patients, there is nothing to delete.
            print('No patients to delete.')
            return False
        if self.current_patient and self.current_patient.phn == phn:
            print('Cannot delete the current patient.')
            return False
        for patient in self.patients:
            if patient.phn == phn:
                self.patients.remove(patient)
                print('Patient deleted.')
                return True
        print('Patient not found.')
        return False
    
    def get_current_patient(self):
        if not self.check_login('get the current patient'):
            return None
        return self.current_patient
    
    def set_current_patient(self, phn):
        if not self.check_login('set the current patient'):
            return False
            
        # check if the patient exists in the list of patients (this is done via PHN).
        for patient in self.patients:
            if patient.phn == phn:
                self.current_patient = patient
                print(f'Current patient set to {self.current_patient.name}.')
                return True
        print('Patient not found.')
        return False

    
    
    def unset_current_patient(self):
        if not self.check_login('unset the current patient'):
            return False
        self.current_patient = None
        return True
    
    def create_note(self, text):
        if self.locked:
            print('You must be logged in to create a note.')
            return None
        if not self.current_patient:
            print('No current patient set.')
            return None
        #create a note and add it to the patient (via patient -> patient record)
        note = self.current_patient.add_note(text)
        #print('Note created.')
        #print(f'Note {note.code}: "{note.text}" Time: {note.timestamp}')
        return note
    
    def search_note(self, code):
        if not self.check_login('search for a note'):
            return None
        if not self.current_patient:
            print('No current passertTrueatient set.')
            return None
        note = self.current_patient.get_note(code)
        if note:
            print(f'Note found: "{note.text}" Time: {note.timestamp}')
            return note
        print('Note not found.')
        return None
    

    #if one of the patient's notes contains the supplied substring, add it to the results list, and return it. 
    def retrieve_notes(self, search_term):
        if not self.check_login('retrieve notes'):
            return None
        if not self.current_patient:
            print('No current patient set.')
            return None
        
        return self.current_patient.retrieve_notes(search_term)
    
    #updates a note with a supplied code, and a new text.
    def update_note(self, code, text):
        if not self.check_login('update a note'):
            return False
        if not self.current_patient:
            print('No current patient set.')
            return False
        #update the note via the patient.
        if self.current_patient.update_note(code, text):
            print('Note updated.')
            return True
        print('Note not found.')
        return False
    
    #removes a note with a supplied code.
    def delete_note(self, code):
        if not self.check_login('delete a note'):
            return False
        if not self.current_patient:
            print('No current patient set.')
            return False  
        return self.current_patient.delete_note(code) 
    
    #lists notes for the current patient.
    def list_notes(self):
        if not self.check_login('list notes'):
            return None
        if not self.current_patient:
            print('No current patient set.')
            return None
        print("Listing notes:")
        return self.current_patient.list_notes()