from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from PyQt6 import uic, QtWidgets

from clinic.controller import Controller


class MainGUI(QtWidgets.QMainWindow):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("SENG265 - Patient Software 2024")
        self.setGeometry(100, 100, 800, 600)

        self.window = uic.loadUi('clinic/gui/main.ui')
        self.setCentralWidget(self.window)
        self.window.show()


        #load the patient data
        

    def load_patient_data(self):
        #load the patient data
        patients = self.controller.list_patients()
        #load into the table
        
        







        
