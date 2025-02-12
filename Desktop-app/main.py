import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from DB_structure import verify_user

#======== load login.ui file=========#
FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'login.ui'))

#========== load dashboard.py file==========#
from dashboard import Dashboard

#========== MainApp class==========#
class MainApp(QWidget, FormClass):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_buttons()

    #========== Database Section==========#
    def Db_Connection(self):
        pass

    #========== Patients Section==========#
    def Show_All_Patients(self):
        pass

    def Add_Patient(self):
        pass

    def Edit_Patient(self):
        pass

    def Delete_Patient(self):
        pass


    #========== handle ui==========#  
    def Handle_Ui(self):
        self.setWindowTitle("Clinic Management System")
         
        #========== hide password==========#
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        
    #========== handle buttons==========#
    def Handle_buttons(self):
        #========== login button==========#
        self.pushButton_login.clicked.connect(self.login)

    #========== login function==========#
    def login(self):
        #========== get username and password==========#
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()

        #========== get role (Doc OR Assist)==========#
        if self.radioButton_doctor.isChecked():
            role = "Doctor"
        elif self.radioButton_assistant.isChecked():
            role = "Assistant"
        else:
            role = None
        #========== check if username and password are empty==========#
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password")
            return
        #========== verify user==========#
        if verify_user(username, password, role):
            QMessageBox.information(self, "Login Success", f"Welcome Ya {role}😎 !")
            #========== open dashboard==========#
            self.dashboard = Dashboard(role)
            self.dashboard.show()
            self.close()  # close login window
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

        #========== clear inputs==========#
        self.lineEdit_username.clear()
        self.lineEdit_password.clear()
        self.radioButton_doctor.setChecked(True)
        self.lineEdit_username.setFocus()

#========== main function==========#
def main():
    app = QApplication(sys.argv)
    style_file = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(style_file):
        with open(style_file, "r") as file:
            app.setStyleSheet(file.read())
    
    login_window = MainApp()
    login_window.show()
    sys.exit(app.exec_())

#========== run main function==========#
if __name__ == '__main__':
    main()  