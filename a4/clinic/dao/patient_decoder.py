import json
from clinic.patient import Patient

class PatientDecoder:
    
    
    @staticmethod
    def decode(json_string) -> dict[int, Patient]:
        def patient_hook(dct):
            if 'phn' in dct and 'name' in dct:
                return Patient(dct['phn'], dct['name'], dct['birth_date'], dct['phone'], dct['email'], dct['address'])
            return dct

        data = json.loads(json_string, object_hook=patient_hook)
        patients = {patient.phn: patient for patient in data.values()}
        # for phn, patient in patients.items():
        #     print(f'Loaded patient: {{{patients[phn].name} - {patients[phn].phn}}}')
        return patients