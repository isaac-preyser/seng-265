import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont


# Add the parent directory of the clinic package to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clinic.gui.main_gui import MainGUI



class LoginGUI(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Continue here with your code!
        self.setWindowTitle("SENG265 - Patient Software 2024")
        self.setGeometry(100, 100, 400, 200)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        #set background color   
        central_widget.setStyleSheet("background-color: #f0f0f0")

        self.message = QLabel("Welcome to the SENG265 Clinic!")
        self.message.setFont(QFont("Arial", 12))
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.message)

        form_layout = QGridLayout()

        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont("Arial", 10))
        form_layout.addWidget(username_label, 0, 0)
        form_layout.addWidget(self.username_input, 0, 1)
        
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        #when the user presses enter on the username field, move the cursor to the password field
        self.username_input.returnPressed.connect(self.password_input.setFocus)

        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)


        main_layout.addLayout(form_layout)

        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 10))
        login_button.setFixedWidth(100)
        login_button.clicked.connect(self.login)
        #or, when the enter button is pressed, trigger the login event. 
        self.password_input.returnPressed.connect(login_button.click)


        main_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        version_label = QLabel("Version 1.0")
        #make the text small
        version_label.setFont(QFont("Arial", 8))
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(version_label)

        


    def login(self, event):
        # This method will be called when the user clicks the login button.
        # It will check the username and password fields, and call login via the controller.
        # If login is successful, the dialog will close, and the main application window will open.
        # If login is unsuccessful, the message will be updated with "Login failed.", etc. 
        
        #get the username and password entered by the user
        username = self.username_input.text()
        password = self.password_input.text()   
        print(f'Username: {username}, Password: {password}')

        #check if the username and password are correct, via the controller.
        try: 
            self.controller.login(username, password)
            #if the login is successful, close the login dialog and open the main application window.

            self.main_window = MainGUI(self.controller)
            self.main_window.show()

            self.hide()

            


        except Exception as e:
            #if the login fails, update the message label with the error message.
            self.message.setText(str(e))







