# FILE: clinic/dao/patient_encoder.py
import json
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.note import Note

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
        if isinstance(o, NoteDAOPickle):
            return None # exclude NoteDAOPickle from the JSON encoding
        if isinstance(o, Note):
            return o.__dict__
        #if the object is a datetime object, convert it to a string
        if hasattr(o, 'isoformat'):
            return o.isoformat()
        return super().default(o)