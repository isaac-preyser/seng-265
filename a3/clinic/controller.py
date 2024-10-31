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
    
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if self.locked:
            print('You must be logged in to create a patient.')
            return None #no operation performed. 
        #make a new patient object
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        for patient in self.patients:
            if patient.phn == new_patient.phn:
                print('Patient already exists.')
                return None #this nehavior might not be desirable.
        self.patients.append(new_patient)
        print('Patient created.')
        return new_patient
    
    def search_patient(self, phn):
        if self.locked:
            print('You must be logged in to search for a patient.')
            return None
        for patient in self.patients:
            if patient.phn == phn:
                print('Patient found.')
                return patient
        print('Patient not found.')
        return None
    
    #this function returns a list of patients that have names that contain the supplied substring (search_term)
    def retrieve_patients(self, search_term):
        if self.locked:
            print('You must be logged in to retrieve patients.')
            return None
        results = []
        for patient in self.patients:
            if search_term in patient.name:
                results.append(patient)
        return results

    def update_patient(self, phn, new_phn, name, birth_date, phone, email, address):
        if self.locked:
            print('You must be logged in to update a patient.')
            return False
        if not self.patients:
            print('No patients to update.')
            return False
        
        patient_to_update = None
        for patient in self.patients:
            if patient.phn == phn:
                patient_to_update = patient
                break
        
        if not patient_to_update:
            print('Patient not found.')
            return False
        
        if patient_to_update == self.current_patient:
            #cannot update the current patient.
            print('Cannot update the current patient.')
            return False

        for patient in self.patients:
            if patient.phn == new_phn and patient.phn != phn:
                print('Patient with new PHN already exists. Cannot update.')
                return False
        
        patient_to_update.phn = new_phn
        patient_to_update.name = name
        patient_to_update.birth_date = birth_date
        patient_to_update.phone = phone
        patient_to_update.email = email
        patient_to_update.address = address
        print('Patient updated.')
        return True
    
    def list_patients(self):
        if self.locked:
            print('You must be logged in to list patients.')
            return None
        #print('Patients:')
        # for patient in self.patients:
        #     print(patient.name)
        return self.patients #returns a list of patients.
    
    def delete_patient(self, phn):
        if self.locked:
            print('You must be logged in to delete a patient.')
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
        if self.locked:
            print('You must be logged in to get the current patient.')
            return None
        return self.current_patient
    
    def set_current_patient(self, phn):
        if self.locked:
            print('You must be logged in to set the current patient.')
            return False
            
        # check if the patient exists in the list of patients (this is done via PHN).
        for patient in self.patients:
            if patient.phn == phn:
                self.current_patient = patient
                print('Current patient set.')
                return True
        print('Patient not found.')
        return False

    
    
    def unset_current_patient(self):
        if self.locked:
            print('You must be logged in to unset the current patient.')
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
        #create a note and add it to the patient record (via the patient record)
        note = self.current_patient.record.add_note(text)
        print('Note created.')
        print(f'Note {note.code}: "{note.text}" Time: {note.timestamp}')
        return note
    
    def search_note(self, code):
        if self.locked:
            print('You must be logged in to search for a note.')
            return None
        if not self.current_patient:
            print('No current patient set.')
            return None
        for note in self.current_patient.record.notes:
            if note.code == code:
                print('Note found.')
                return note
        print('Note not found.')
        return None
    

    #if one of the patient's notes contains the supplied substring, add it to the results list, and return it. 
    def retrieve_notes(self, search_term):
        if self.locked:
            print('You must be logged in to retrieve notes.')
            return None
        if not self.current_patient:
            print('No current patient set.')
            return None
        
        return self.current_patient.search_notes(search_term)
