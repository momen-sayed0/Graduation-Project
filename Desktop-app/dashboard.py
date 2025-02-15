import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from CRUDOperations import CRUDOperations

FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

class Dashboard(QMainWindow, FormClass):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.role = role

        self.setWindowTitle("Dashboard - Clinic Management System")
        self.stackedWidget.setCurrentIndex(0) 
        self.patient_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Disease_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.report_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.logout_btn.clicked.connect(self.logout)
        self.add_patient.clicked.connect(self.add_new_patient)  # ربط زر الإضافة بالدالة
        self.pushButton.clicked.connect(self.show_all_patients)  # زر عرض جميع المرضى


        self.configure_permissions()
        self.show_all_patients()

    def configure_permissions(self):
        if self.role == "Assistant":
            self.Disease_btn.hide()
    
        if self.role == "Doctor":
            self.tabWidget_2.removeTab(0)

    def add_new_patient(self):
        """إضافة مريض جديد إلى قاعدة البيانات"""
        name = self.lineEdit_2.text().strip()
        date_of_birth = self.dateEdit.date().toString("yyyy-MM-dd")
        gender = self.comboBox.currentText()
        phone = self.lineEdit_9.text().strip()
        address = self.textEdit.toPlainText().strip()
        
        if not name or not phone or not address:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        result = CRUDOperations.add_patient(name, date_of_birth, gender, phone, address)
        
        if result['success']:
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.clear_patient_fields()
        else:
            QMessageBox.critical(self, "Error", f"Failed to add patient: {result['message']}")

    def show_all_patients(self):
        """عرض جميع المرضى في الجدول"""
        patients = CRUDOperations.get_all_patients()
        if isinstance(patients, dict) and not patients.get('success', True):
            QMessageBox.critical(self, "Error", f"Failed to fetch patients: {patients['message']}")
            return
        
        self.tableWidget.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(patient['id'])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(patient['name']))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(patient['date_of_birth'])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(patient['gender']))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(patient['phone']))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(patient['address']))


    def clear_patient_fields(self):
        """تفريغ الحقول بعد الإضافة الناجحة"""
        self.lineEdit_2.clear()
        self.lineEdit_9.clear()
        self.textEdit.clear()
        self.comboBox.setCurrentIndex(0)
        self.dateEdit.setDate(self.dateEdit.minimumDate())

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
