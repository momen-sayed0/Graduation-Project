import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType


FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

class Dashboard(QMainWindow, FormClass):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.role = role

        self.stackedWidget.setCurrentIndex(0) 
        self.patient_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Disease_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.report_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.logout_btn.clicked.connect(self.logout)

        self.configure_permissions()

    def configure_permissions(self):
        if self.role == "Assistant":
            self.Disease_btn.hide()
    
        if self.role == "Doctor":
            self.tabWidget_2.removeTab(0)

    def logout(self):
        self.close()
        from main import LoginWindow 
        self.login_window = LoginWindow () 
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard("Doctor")
    window.show()
    sys.exit(app.exec_())
