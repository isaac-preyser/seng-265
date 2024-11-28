import sys
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.uic as uic
from PyQt6.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from clinic.controller import Controller

class NoteTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # return the note code and text
            if index.column() == 0:
                return self._data[index.row()].code
            elif index.column() == 1:
                return str(self._data[index.row()].timestamp)
            else: 
                return None

        
        
    def rowCount(self, index):
        # return the number of notes in the list. 
        return len(self._data)
    
    def columnCount(self, index):
        # Note code, timestamp. 
        return 2 #might want to change to 2, and have the vert header data contain the note codes. 
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == 0:
                    return 'Code'
                elif section == 1:
                    return 'Timestamp'
                else:
                    return None

            else:
                return section
        return None

    


class PatientTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # return the patient name and PHN
            return self._data[index.row()].name if index.column() == 0 else self._data[index.row()].phn

    def get_phn(self, row):
        return self._data[row].phn

    def rowCount(self, index):
        # return the number of patients in the list. 
        return len(self._data)
    
    def columnCount(self, index):
        return 2 #name and PHN only. 
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return 'Name' if section == 0 else 'PHN'
            else:
                return section + 1
        return None
 
class MainGUI(QtWidgets.QMainWindow):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("SENG265 - Patient Software 2024")
        self.setGeometry(100, 100, 800, 600)

        # load the UI directly into self
        uic.loadUi('clinic/gui/main.ui', self)

        self.statusBar().showMessage(f'Welcome, {self.controller.current_user}')

        # load the patient data
        self.patientsList = self.findChild(QtWidgets.QWidget, 'patientsList')
        # set the model for the patients list
        self.patientsList.setModel(PatientTableModel(self.controller.list_patients()))
         # resize the columns to fit the data. 
        self.patientsList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.patientsList.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # whenever a row is selected, update the current patient
        self.patientsList.selectionModel().selectionChanged.connect(self.update_current_patient)


        self.notesList = self.findChild(QtWidgets.QTableView, 'notesList')
        self.notesList.setModel(NoteTableModel([]))
        # when a patient row is selected, update the notes list. 
        self.patientsList.selectionModel().selectionChanged.connect(self.update_notes_list)
        # resize the columns to fit the data. 
        self.notesList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        




        # connect the patientSearchBar to the search_patient method
        self.patientSearchBar = self.findChild(QtWidgets.QLineEdit, 'patientSearchBar')
        self.patientSearchBar.textChanged.connect(self.search_patient)

        # connect the addPatientButton to the new_patient method
        self.addPatientButton = self.findChild(QtWidgets.QPushButton, 'addPatientButton')
        self.addPatientButton.clicked.connect(self.new_patient)


        # connect the notes search bar to the search_notes method
        # when a note is selected, update the note text box.

        # when a note is selected, update the note text box.
        self.notesList.selectionModel().selectionChanged.connect(self.update_current_note)

        # TODO: Fix the above connection; it is not working. 




        # show the main window
        self.show()

    def update_current_patient(self, newSelection):
        # get the selected row, if it is non-empty
        if newSelection.indexes():
            selectedRow = newSelection.indexes()[0].row()
            print(f'Row {selectedRow} selected.')

            #highlight the selected row
            self.highlight_row(selectedRow)


            # get the PHN of the selected patient
            phn = self.patientsList.model().get_phn(selectedRow)
            print(f'PHN: {phn}')
            # set the current patient
            if self.controller.set_current_patient(phn):
                #print(f'Current patient set - {self.controller.current_patient}')
                pass
            
    def highlight_row(self, row):
        selectionModel = self.patientsList.selectionModel()
        selection = QItemSelection(self.patientsList.model().index(row, 0), self.patientsList.model().index(row, 1))
        selectionModel.select(selection, QItemSelectionModel.SelectionFlag.Select)
        self.patientsList.selectionModel().setCurrentIndex(self.patientsList.model().index(row, 0), QItemSelectionModel.SelectionFlag.SelectCurrent)



    def update_current_patient_info(self):
        # on the second tab, update the current patient's information.
        pass

    def contains_subinteger(self, main_int, sub_int):
        #helper for searching by PHN
        return str(sub_int) in str(main_int)

    def update_patient_list(self, patient_list):
        # Update the model
        self.patientsList.model().beginResetModel()
        self.patientsList.model()._data = patient_list
        self.patientsList.model().endResetModel()

        # Clear the current patient
        self.controller.current_patient = None
        self.update_current_patient_info()

    def search_patient(self):
        # Accept text input from the search bar, filter the patient list.
        search_term = self.patientSearchBar.text()

        # If the search term is numeric, search by PHN.
        if search_term.isnumeric():
            search_term = int(search_term)
            patient_list = []
            for patient in self.controller.list_patients():
                if self.contains_subinteger(patient.phn, search_term):
                    patient_list.append(patient)
        else:
            search_term = search_term.strip()
            # Get the patient list
            patient_list = self.controller.retrieve_patients(search_term)

        # Update the patient list
        self.update_patient_list(patient_list)


    def new_patient(self):
        # Create a new patient
        try:
            # get the length of the current patient list, and add 1
            phn = len(self.controller.list_patients()) + 1 # this is a placeholder for the PHN
            name = f'New Patient {phn}'
            birth_date = '0000-00-00'
            phone = '000-000-0000'
            email = 'please enter an email'
            address = 'please enter an address'
            self.controller.create_patient(phn, name, birth_date, phone, email, address)
        except Exception as e:
            print(f'Error: {e}')

        # Update the patient list
        self.search_patient() # this will update the patient list with the new patient

    def update_notes_list(self):
        if self.controller.current_patient is None:
            print('No current patient.')
            return
        # Get the current patient's notes
        notes = self.controller.current_patient.list_notes()
        # Update the notes list
        self.notesList.setModel(NoteTableModel(notes))

    def search_notes(self, text):
        if self.controller.current_patient is None:
            print('No current patient.')
            return
        # Get the current patient's notes
        notes = self.controller.current_patient.retrieve_notes(text)
        # Update the notes list
        self.notesList.setModel(NoteTableModel(notes))

    def update_current_note(self, newSelection):
        print(f'Note selected: {newSelection.indexes()}')
        if newSelection.indexes():
            selectedRow = newSelection.indexes()[0].row()
            self.noteContent = self.findChild(QtWidgets.QLabel, 'noteContent')
            self.noteContent.setText(self.controller.current_patient.list_notes()[selectedRow].text)