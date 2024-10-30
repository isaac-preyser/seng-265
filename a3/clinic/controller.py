from clinic.patient import Patient

class Controller: 
    def __init__(self):
        self.locked = True
        self.patients = []
        #user/password for login. consider changing the init function to take arguments to do a constructor here. 
        self.password = 'clinic2024' #default password  
        self.user = 'user' #default user

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
        
    