import sys
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.uic as uic
from PyQt6.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

from clinic.controller import Controller

class NoteTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data   

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # return the note code and text
            return self._data[index.row()].code if index.column() == 0 else self._data[index.row()].text
        
    def rowCount(self, index):
        # return the number of notes in the list. 
        return len(self._data)
    
    def columnCount(self, index):
        # Note code, timestamp, and text. 
        return 3 #might want to change to 2, and have the vert header data contain the note codes. 
    




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
        # whenever a row is selected, update the current patient
        self.patientsList.selectionModel().selectionChanged.connect(self.update_current_patient)
        # when that row is selected, load the notes. 
        self.notesList = self.findChild(QtWidgets.QTableView, 'notesList')





        # connect the patientSearchBar to the search_patient method
        self.patientSearchBar = self.findChild(QtWidgets.QLineEdit, 'patientSearchBar')
        self.patientSearchBar.textChanged.connect(self.search_patient)

        # connect the addPatientButton to the new_patient method
        self.addPatientButton = self.findChild(QtWidgets.QPushButton, 'addPatientButton')
        self.addPatientButton.clicked.connect(self.new_patient)








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
            self.controller.set_current_patient(phn)

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

