from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient

class PatientDAOJSON(PatientDAO):
    def __init__(self):
        self._patients = []

    def __iter__(self):
        return iter(self.patients.values())

    def search_patient(self, phn) -> Patient:
        return self.get_patient(phn)
        
    def create_patient(self, phn, name, birth_date, phone, email, address):
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        self._patients.append(new_patient)
        return new_patient

    def retrieve_patients(self, search_string) -> list[Patient]:
        results = []
        for patient in self._patients:
            if search_string in patient.name:
                results.append(patient)
        return results

    def get_patient(self, phn: str) -> Patient:
        for patient in self._patients:
            if patient.phn == phn:
                return patient
        return None

    def update_patient(self, key, patient) -> Patient:
        for i, p in enumerate(self._patients):
            if p.phn == key:
                self._patients[i] = patient
                return patient

    def delete_patient(self, key):
        self._patients = [p for p in self._patients if p.phn != key]
        return True

    def list_patients(self) -> list[Patient]:
        return self._patients