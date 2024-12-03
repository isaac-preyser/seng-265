import sys
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.uic as uic
from PyQt6.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt6.QtGui import QKeySequence, QShortcut
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
                # return the first 25 characters of the note text
                return (self._data[index.row()].text[:25] + '...') if len(self._data[index.row()].text) > 50 else self._data[index.row()].text
            elif index.column() == 1:
                #show the date and time, no seconds or below.
                return str(self._data[index.row()].timestamp.strftime('%Y-%m-%d %H:%M'))
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
                    return 'Text Preview'
                elif section == 1:
                    return 'Timestamp'
                else:
                    return None
            if orientation == Qt.Orientation.Vertical:
                return self._data[section].code
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
        self.notesList.setModel(NoteTableModel([])) # use an empty list, and then update it when a patient is selected.
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

        # connect the note search bar to the search_notes method
        self.noteSearchBar = self.findChild(QtWidgets.QLineEdit, 'noteSearchBar')
        self.noteSearchBar.textChanged.connect(self.search_notes)
        # when a note is selected, update the note text box.
        self.notesList.selectionModel().selectionChanged.connect(self.display_selected_note)
        #also change the preview text of updateNoteField to the selected note's text (for editing)
        self.updateNoteField = self.findChild(QtWidgets.QPlainTextEdit, 'updateNoteField')
        # when CTRL+Enter is pressed, update the note.
        self.updateNoteShortcut = QShortcut(QKeySequence('Ctrl+Return'), self.updateNoteField)
        self.updateNoteShortcut.activated.connect(self.update_note)
        #this will be done in the display_selected_note method, we just needed to have a reference to the field (as acheived above.)

        #connect the noteContent to the noteContent label
        self.noteContent = self.findChild(QtWidgets.QLabel, 'noteContent')
        self.noteInfoBar = self.findChild(QtWidgets.QLabel, 'noteInfoBar')



        #connect the updateNoteButton to the update_note method
        self.updateNoteButton = self.findChild(QtWidgets.QPushButton, 'updateNoteButton')
        self.updateNoteButton.clicked.connect(self.update_note)


        #populate the current patient info line edits
        self.patientData_address = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_address')
        self.patientData_address.setPlainText('Select a patient to view their information.')


        self.patientData_birth = self.findChild(QtWidgets.QLineEdit, 'lineEdit_birth')
        
        self.patientData_email = self.findChild(QtWidgets.QLineEdit, 'lineEdit_email')
        
        self.patientData_name = self.findChild(QtWidgets.QLineEdit, 'lineEdit_name')
        
        self.patientData_phone = self.findChild(QtWidgets.QLineEdit, 'lineEdit_phone')
        
        self.patientData_phn = self.findChild(QtWidgets.QLineEdit, 'lineEdit_phn')
        
        # populate the current patient buttonbox

        self.patientData_buttons = self.findChild(QtWidgets.QDialogButtonBox, 'patientData_buttons')

        # connect the buttons to the appropriate methods. 

        #reset the current patient's information
        self.patientData_buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Reset).clicked.connect(self.update_current_patient_info)

        #save the current patient's information, based on the data in the line edits.
        self.patientData_buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Save).clicked.connect(self.save_current_patient_info)

        #connect the discard button to the delete_patient method
        self.patientData_buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Discard).clicked.connect(self.delete_patient)
        #connect the "-" button to the delete_patient method
        self.deletePatientButton = self.findChild(QtWidgets.QPushButton, 'deletePatientButton')
        if not self.deletePatientButton:
            print('Delete patient button not found.')
        self.deletePatientButton.clicked.connect(self.delete_patient)


        #connect the addNoteButton to the add_note method
        self.addNoteButton = self.findChild(QtWidgets.QPushButton, 'addNoteButton')
        self.addNoteButton.clicked.connect(self.add_note)

        #connect the deleteNoteButton to the delete_note method
        self.deleteNoteButton = self.findChild(QtWidgets.QPushButton, 'deleteNoteButton')
        self.deleteNoteButton.clicked.connect(self.delete_note)

        #connect the logout_button to the logout method
        self.logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button')
        self.logout_button.clicked.connect(self.controller.logout)


        # show the main window
        self.show()



    def logout(self):
        #open a dialog box to confirm the logout
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle('Logout')
        dialog.setText('Are you sure you want to logout?')
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        response = dialog.exec()
    
        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            #logout
            self.controller.logout()
            self.main_window.close()
            

        else:
            #show a notification that the logout was cancelled in the status bar. 
            self.statusBar().showMessage('Logout cancelled')
                                         



        

    
    def add_note(self):
        if self.controller.current_patient is None:
            self.statusBar().showMessage('No patient selected. Please select a patient to add a note.')
            return
        #show a dialog box to get the note text
        dialog = QtWidgets.QInputDialog()
        dialog.setWindowTitle('Add Note')
        dialog.setLabelText('Enter the note text:')
        dialog.setOkButtonText('Add Note')
        dialog.setCancelButtonText('Cancel')
        response = dialog.exec()
        if response == QtWidgets.QDialog.DialogCode.Accepted:
            note_text = dialog.textValue()
            #add the note to the current patient
            self.controller.create_note(note_text)
            #update the notes list
            self.update_notes_list()
            #show a notification that the note was added in the status bar. 
            self.statusBar().showMessage(f'Note added to {self.controller.current_patient.name}.')
        else:
            #show a notification that the addition was cancelled in the status bar. 
            self.statusBar().showMessage('Note addition cancelled')

    def delete_patient(self):
        if self.controller.current_patient is None:
            self.statusBar().showMessage('No patient selected. Please select a patient to delete.')
            return
    
        #show a dialog box to confirm the deletion of the patient.
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle('Delete Patient')
        dialog.setText(f'Are you sure you want to delete {self.controller.current_patient.name}?')
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        response = dialog.exec()

        patient_name = self.controller.current_patient.name
        phn = self.controller.current_patient.phn

        #if the user confirms the deletion, delete the patient.
        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            #unset the current patient
            phn_to_delete = self.controller.current_patient.phn
            self.controller.current_patient = None
            if self.controller.delete_patient(phn_to_delete):
                #show a notification that the patient was deleted in the status bar. 
                self.statusBar().showMessage(f'Patient {patient_name} [{phn}] deleted.')
                #update the patient list
                self.update_patient_list(self.controller.list_patients())
                #clear the current patient's information
                self.controller.current_patient = None
                self.update_current_patient_info()
                #clear the notes list
                self.notesList.setModel(NoteTableModel([]))
                #clear the note text box
                self.noteContent.setText('')
                self.updateNoteField.setPlainText('')
                self.noteInfoBar.setText('Select a note to view or update.')
                #clear the search bar
                self.noteSearchBar.setText('')
        else: 
            #show a notification that the deletion was cancelled in the status bar. 
            self.statusBar().showMessage('Deletion cancelled')

        

    def save_current_patient_info(self):
        # get the current patient's information from the line edits
        old_phn = self.controller.current_patient.phn
        new_phn = self.patientData_phn.text().strip()
        name = self.patientData_name.text().strip()
        birth_date = self.patientData_birth.text().strip()
        phone = self.patientData_phone.text().strip()
        email = self.patientData_email.text().strip()
        address = self.patientData_address.toPlainText().strip()

        #unset the current patient
        self.controller.current_patient = None

        # update the current patient's information
        self.controller.update_patient(old_phn, new_phn, name, birth_date, phone, email, address)
        
        #set the current patient to the updated patient
        self.controller.set_current_patient(new_phn)
        
        # update the patient list
        self.update_patient_list(self.controller.list_patients())


        # update the current patient's information
        self.update_current_patient_info()
        # show a notification that the patient was updated in the status bar. 
        self.statusBar().showMessage(f'Patient {name} updated.')

        return    

    def update_current_patient(self, newSelection):
        # get the selected row, if it is non-empty
        if newSelection.indexes():
            selectedRow = newSelection.indexes()[0].row()
            # print(f'Row {selectedRow} selected.')

            # get the PHN of the selected patient
            phn = self.patientsList.model().get_phn(selectedRow)
            # print(f'PHN: {phn}')
            # set the current patient
            if self.controller.set_current_patient(phn):
                #print(f'Current patient set - {self.controller.current_patient}')
                # update the current patient's information
                self.update_current_patient_info()
                pass

        else:
            # set the current patient to None. 
            self.controller.current_patient = None
            print('No patient selected - setting to None.')
            self.update_current_patient_info()
        
        # update the notes list
        self.update_notes_list()

        #if there is a note currently selected, clear it.
        self.noteContent.setText('')
        self.updateNoteField.setPlainText('')
        self.noteInfoBar.setText('Select a note to view or update.')
        #clear the search bar
        self.noteSearchBar.setText('')

        #clear the notes list
        self.notesList.setModel(NoteTableModel([]))

    def update_current_patient_info(self):
        if self.controller.current_patient is None:
            self.patientData_phn.setText('')
            self.patientData_name.setText('')
            self.patientData_birth.setText('')
            self.patientData_phone.setText('')
            self.patientData_email.setText('')
            self.patientData_address.setPlainText('Select a patient to view their information.')
            return
        
        
        self.patientData_phn.setText(str(self.controller.current_patient.phn))
        self.patientData_name.setText(self.controller.current_patient.name)
        self.patientData_birth.setText(self.controller.current_patient.birth_date)
        self.patientData_phone.setText(self.controller.current_patient.phone)
        self.patientData_email.setText(self.controller.current_patient.email)
        self.patientData_address.setPlainText(self.controller.current_patient.address)

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
        # when a note is selected, update the note text box.
        self.notesList.selectionModel().selectionChanged.connect(self.display_selected_note)


    def search_notes(self, text):
        if self.controller.current_patient is None:
            print('No current patient.')
            return
        
        #if the search bar is numeric, search by note code
        if text.isnumeric():
            sub_code = int(text)
            notes = []
            for note in self.controller.current_patient.list_notes():
                if self.contains_subinteger(note.code, sub_code):
                    notes.append(note)
            # if we find no notes, try to search by date. 
            if len(notes) == 0:
                for note in self.controller.current_patient.list_notes():
                    if self.contains_subinteger(note.timestamp, sub_code):
                        notes.append(note)
        #otherwise, search by note text.
        else:
            text = text.strip()
             # Get the current patient's notes
            notes = self.controller.current_patient.retrieve_notes(text)

        # Update the notes list 
        self.notesList.setModel(NoteTableModel(notes))

    def display_selected_note(self, newSelection):
        print(f'Note selected: {newSelection.indexes()}')
        if newSelection.indexes():
            selectedRow = newSelection.indexes()[0].row()
            self.noteContent.setText(self.controller.current_patient.list_notes()[selectedRow].text)
            self.updateNoteField.setPlainText(self.controller.current_patient.list_notes()[selectedRow].text)
            self.noteInfoBar.setText(f'[{self.controller.current_patient.name}] Note {self.controller.current_patient.list_notes()[selectedRow].code} - {self.controller.current_patient.list_notes()[selectedRow].timestamp.strftime("%Y-%m-%d %H:%M")}')    
        else:
            self.noteContent.setText('')
            self.updateNoteField.setPlainText('')
            self.noteInfoBar.setText('Select a note to view or update.')

    def delete_note(self):
        
        
        # get the selected note
        selectedRow = self.notesList.selectionModel().selectedRows()
        if not selectedRow:
            print('No note selected.')
            self.statusBar().showMessage('No note selected. Please select a note to delete.')
            return
        selectedRow = selectedRow[0].row()
        note = self.controller.current_patient.list_notes()[selectedRow]

        #display a dialog box to confirm the deletion of the note.
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle('Delete Note')
        dialog.setText(f'Are you sure you want to delete Note {note.code}?')
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        response = dialog.exec()

        #if the user confirms the deletion, delete the note.
        if response == QtWidgets.QMessageBox.StandardButton.Yes:            
            # delete the note
            self.controller.delete_note(note.code)
            # update the notes list
            self.update_notes_list()
            # clear the note text box
            self.noteContent.setText('')
            self.updateNoteField.setPlainText('')
            self.noteInfoBar.setText('Select a note to view or update.')
            # show a notification that the note was deleted in the status bar. 
            self.statusBar().showMessage(f'Note {note.code} deleted.')

        else:
            #show a notification that the deletion was cancelled in the status bar. 
            self.statusBar().showMessage('Deletion cancelled')

    def update_note(self):
        # get the selected note
        selectedRow = self.notesList.selectionModel().selectedRows()
        if not selectedRow:
            print('No note selected.')
            self.statusBar().showMessage('No note selected. Please select a note to update.')
            return
        selectedRow = selectedRow[0].row()
        note = self.controller.current_patient.list_notes()[selectedRow]
        # get the new note text
        new_text = self.updateNoteField.toPlainText()
        # update the note
        self.controller.update_note(note.code, new_text)
        # update the notes list
        self.update_notes_list()
        # keep the current note selected. 
        self.notesList.selectRow(selectedRow)

        #update the note text box
        self.noteContent.setText(new_text) #this is poor code practice. 


        #show a notification that the note was updated in the status bar. 
        self.statusBar().showMessage(f'Note {note.code} updated.')
        