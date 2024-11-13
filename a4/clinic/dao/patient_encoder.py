# FILE: clinic/dao/patient_encoder.py
import json
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.dao.note_dao_pickle import NoteDAO

class PatientEncoder(json.JSONEncoder):
    """
    PatientEncoder is a custom JSON encoder for serializing Patient objects.
    It extends json.JSONEncoder and overrides the default method to convert Patient instances to dictionaries.
    """
    def default(self, o):
        if isinstance(o, Patient):
            return o.__dict__
        if isinstance(o, PatientRecord):
            return o.__dict__
        if isinstance(o, NoteDAO):
            return o.__dict__
        
        return super().default(o)