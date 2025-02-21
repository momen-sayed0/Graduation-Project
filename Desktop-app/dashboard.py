import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox

from PyQt5.uic import loadUiType
from Database import DatabaseConnection
from patient_manager import PatientManager, PatientViewHandler

FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

# Apply QSS file for styling
def apply_stylesheet(app, qss_file):
    if os.path.exists(qss_file):
        with open(qss_file, "r") as file:
            app.setStyleSheet(file.read())

class Dashboard(QMainWindow, FormClass):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.role = role

        self.setWindowTitle("Dashboard - Clinic Management System")

        # Create an object to manage the database connection
        self.db_manager = DatabaseConnection()
        self.db_manager.connect()

        # Create an object to manage patient data (add, view, delete, search, and modify)
        self.patient_manager = PatientManager(self)
        # Show patients when pressing patient_btn button
        self.patient_view_handler = PatientViewHandler(self)

        self.configure_permissions()

        self.stackedWidget.setCurrentIndex(0)
        self.dashboard_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.patient_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.chest_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.brain_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.eye_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.heart_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.chatbot_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.report_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.logout_btn.clicked.connect(self.logout)


        # Link reload button
        if hasattr(self, "reload_btn"):
            self.reload_btn.clicked.connect(self.patient_manager.load_all_patients)
        # Search button
        if hasattr(self, "pushButton"):
            self.pushButton.clicked.connect(self.patient_manager.search_patient)


    def configure_permissions(self):
        if self.role == "Assistant":
            self.Disease_btn.hide()
    
        if self.role == "Doctor":
            self.tabWidget_2.removeTab(0)


    def logout(self):
        self.db_manager.close()
        self.close()
        from main import LoginWindow 
        self.login_window = LoginWindow() 
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard("Doctor")
    apply_stylesheet(app, "app_style.qss")
    window.show()
    sys.exit(app.exec_())
