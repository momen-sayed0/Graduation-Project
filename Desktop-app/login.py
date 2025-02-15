import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from auth import verify_user
from dashboard import Dashboard

#======== load login.ui file =========#
FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'login.ui'))

#========== LoginWindow class ==========#
class LoginWindow(QWidget, FormClass):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_buttons()

    #========== handle ui ==========#  
    def Handle_Ui(self):
        self.setWindowTitle("Login - Clinic Management System")
        self.setup_password_field()
        self.setup_validators()
        self.setup_icons()  

        #========== set default role to Doctor ==========#
        self.radioButton_doctor.setChecked(True)
   
    #========== handle buttons ==========#
    def Handle_buttons(self):
        self.pushButton_login.clicked.connect(self.login)
        self.togglePasswordButton.clicked.connect(self.toggle_password_visibility)
        #========== clear errors when typing ==========#
        self.lineEdit_username.textChanged.connect(self.clear_username_error)
        self.lineEdit_password.textChanged.connect(self.clear_password_error)
    
    #========== setup password field with toggle button ==========#
    def setup_password_field(self):
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.togglePasswordButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/eye_closed.png")))

    #========== setup icons inside QLineEdit ==========#
    def setup_icons(self):
        icon_path_user = os.path.join(os.path.dirname(__file__), "icons/user.png")
        icon_path_pass = os.path.join(os.path.dirname(__file__), "icons/password.png")

        if not os.path.exists(icon_path_user):
            print("Error: User icon file not found!")
        if not os.path.exists(icon_path_pass):
            print("Error: Password icon file not found!")

        username_icon = QIcon(icon_path_user)
        password_icon = QIcon(icon_path_pass)

        if not username_icon.isNull():
            self.lineEdit_username.addAction(username_icon, QLineEdit.LeadingPosition)
        if not password_icon.isNull():
            self.lineEdit_password.addAction(password_icon, QLineEdit.LeadingPosition)

    #========== toggle password visibility ==========#
    def toggle_password_visibility(self):
        if self.lineEdit_password.echoMode() == QLineEdit.Password:
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
            self.togglePasswordButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/eye_open.png")))
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            self.togglePasswordButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/eye_closed.png")))
    
    #========== setup input validators ==========#
    def setup_validators(self):
        username_validator = QRegularExpressionValidator(QRegularExpression("^[A-Za-z0-9_]+$"))
        self.lineEdit_username.setValidator(username_validator)
        
        password_validator = QRegularExpressionValidator(QRegularExpression("^\\S+$"))
        self.lineEdit_password.setValidator(password_validator)

    #========== validate inputs ==========#
    def validate_inputs(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        self.clear_errors()
        has_error = False

        #========== check username ==========#
        if not username:
            self.label_usernameError.setText("Username cannot be empty")
            self.lineEdit_username.setStyleSheet("border: 2px solid red;")
            has_error = True

        #========== check password ==========#
        if not password:
            self.label_passwordError.setText("Password cannot be empty")
            self.lineEdit_password.setStyleSheet("border: 2px solid red;")
            has_error = True
        elif " " in password:
            self.label_passwordError.setText("Password cannot contain spaces")
            self.lineEdit_password.setStyleSheet("border: 2px solid red;")
            has_error = True

        return not has_error  # return True if no errors

    #========== login function ==========#
    def login(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        role = "Doctor" if self.radioButton_doctor.isChecked() else "Assistant"

        if not self.validate_inputs():
            return  # stop the function if there are errors

        if verify_user(username, password, role):
            QMessageBox.information(self, "Login Success", f"Welcome Ya {role}😎 !")
            self.open_dashboard(role)
        else:
            self.show_login_error()

    #========== open dashboard window ==========#
    def open_dashboard(self, role):
        if hasattr(self, 'dashboard') and self.dashboard is not None:
            self.dashboard.close()
        self.dashboard = Dashboard(role)
        self.dashboard.show()
        self.close()  # close login window

    #========== show login error messages ==========#
    def show_login_error(self):
        self.label_passwordError.setText("Invalid password")
        self.label_usernameError.setText("Invalid username")
        self.lineEdit_username.setStyleSheet("border: 2px solid red;")
        self.lineEdit_password.setStyleSheet("border: 2px solid red;")
        
    #========== clear errors ==========#
    def clear_errors(self):
        self.label_usernameError.setText("")
        self.label_passwordError.setText("")
        self.lineEdit_username.setStyleSheet("")
        self.lineEdit_password.setStyleSheet("")

    def clear_username_error(self):
        self.label_usernameError.setText("")
        self.lineEdit_username.setStyleSheet("")

    def clear_password_error(self):
        self.label_passwordError.setText("")
        self.lineEdit_password.setStyleSheet("")
