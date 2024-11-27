import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

# Add the parent directory of the clinic package to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clinic.gui.login_gui import LoginGUI
from clinic.controller import Controller


class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        




def main():
    app = QApplication(sys.argv)
    #init the controller
    controller = Controller() 
    window = LoginGUI(controller)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
