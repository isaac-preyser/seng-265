import clinic.exception as exception
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient

class PatientDAOJSON(PatientDAO):
    def __init__(self):
        self._patients = {}

    def __iter__(self):
        return iter(self._patients.values())

    def search_patient(self, phn) -> Patient:
        return self.get_patient(phn)
        
    def create_patient(self, phn, name, birth_date, phone, email, address):
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        if new_patient.phn in self._patients:
            #if the PHN is already in use, we cannot create a new patient.
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - PHN already in use.')
        self._patients[new_patient.phn] = new_patient
        return new_patient

    def retrieve_patients(self, search_string) -> list[Patient]:
        results = []
        for patient in self._patients.values():
            if search_string in patient.name:
                results.append(patient)
        return results

    def get_patient(self, phn: str) -> Patient:
        return self._patients.get(phn)

    def update_patient(self, phn, new_phn, name, birth_date, phone, email, address) -> Patient:
        if phn not in self._patients:
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - patient not found.')
        if new_phn != phn and new_phn in self._patients:
            raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - PHN already in use.')
        
        updated_patient = Patient(new_phn, name, birth_date, phone, email, address)
        del self._patients[phn]
        self._patients[new_phn] = updated_patient
        return updated_patient

    def delete_patient(self, key):
        if (key in self._patients):
            del self._patients[key]
            return True
        raise exception.illegal_operation_exception.IllegalOperationException('Illegal operation - PHN not found.')
    

    def list_patients(self) -> list[Patient]:
        return list(self._patients.values())