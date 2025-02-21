from datetime import date
from models import Patients
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton
from PyQt5.QtCore import QDate, QCoreApplication


# =====================================================================
# Add Patient
# Read input data from the user interface (patient addition fields)
# and enter them into the database, as well as clean the fields after addition.
# =====================================================================
class PatientInputHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.add_patient.clicked.connect(self.add_new_patient)

    def add_new_patient(self):
        name = self.ui.lineEdit_2.text().strip()
        dob_str = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        gender = self.ui.comboBox.currentText()
        phone = self.ui.lineEdit_9.text().strip()
        address = self.ui.lineEdit_5.text().strip()

        if not name or not phone or not address:
            QMessageBox.warning(self.ui, "Error", "Please fill in all required fields.")
            return

        try:
            Patients.create(
                name=name,
                date_of_birth=dob_str,
                gender=gender,
                phone=phone,
                address=address
            )
            QMessageBox.information(self.ui, "Success", "Patient added successfully!")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"An error occurred while adding: {e}")

    def clear_fields(self):
        self.ui.lineEdit_2.clear()
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_5.clear()
# =====================================================================
# PatientDeleter
# Delete a patient record from the database from the "Delete" button.
# =====================================================================
class PatientDeleter:
    def __init__(self, ui):
        self.ui = ui

    def delete_patient(self, patient_id):
        reply = QMessageBox.question(
            self.ui,
            "Confirm Delete",
            "Are you sure you want to delete this patient?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                patient = Patients.get(Patients.id == patient_id)
                patient.delete_instance()
                QMessageBox.information(self.ui, "Success", "Patient deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self.ui, "Error", f"An error occurred while deleting the patient: {e}")
# =====================================================================
# PatientEditor
# Upload patient data to the editing interface and save the changes.
# =====================================================================
class PatientEditor:
    def __init__(self, ui):
        self.ui = ui
        self.ui.Save.clicked.connect(self.update_patient)
        self.current_patient_id = None
# Upload selected patient data to update page
    def load_patient_data(self, patient):
        print("Editing patient with ID:", patient.id)
        self.current_patient_id = patient.id
        self.ui.lineEdit_3.setText(patient.name)
        if patient.date_of_birth:
            self.ui.dateEdit_2.setDate(patient.date_of_birth)
        else:
            self.ui.dateEdit_2.setDate(QDate.currentDate())
        self.ui.comboBox_2.setCurrentText(patient.gender)
        self.ui.lineEdit_10.setText(patient.phone)
        self.ui.lineEdit_6.setText(patient.address)
        self.ui.stackedWidget.setCurrentIndex(4)
        QCoreApplication.processEvents()
        print("Switched to Update Patient page at stackedWidget index 4.")

    # Save the user's changes to the patient data,
    # reload the table, and change the page to the Patient View page.
    def update_patient(self):
        if not self.current_patient_id:
            QMessageBox.warning(self.ui, "Error", "No patient selected for update.")
            return

        try:
            patient = Patients.get(Patients.id == self.current_patient_id)
            patient.name = self.ui.lineEdit_3.text().strip()
            dob_str = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
            patient.date_of_birth = dob_str
            patient.gender = self.ui.comboBox_2.currentText()
            patient.phone = self.ui.lineEdit_10.text().strip()
            patient.address = self.ui.lineEdit_6.text().strip()
            patient.save()
            QMessageBox.information(self.ui, "Success", "Patient updated successfully!")
            self.clear_update_fields()
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.patient_manager.load_all_patients()
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"An error occurred while updating: {e}")

    def clear_update_fields(self):
        self.ui.lineEdit_3.clear()
        self.ui.dateEdit_2.setDate(QDate.currentDate())
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_6.clear()
        self.current_patient_id = None


# =====================================================================
# PatientTableManager
# Load patient data from the database and display it in the table
# It also adds "Edit" and "Delete" buttons for each row
# =====================================================================
class PatientTableManager:
    def __init__(self, ui, deleter, editor):
        self.ui = ui
        self.deleter = deleter
        self.editor = editor

    def populate_table(self, patients):
        table = self.ui.tableWidget
        table.clearContents()
        headers = ["ID", "Name", "Age", "Gender", "Phone", "Edit", "Delete"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(0)

        for i, patient in enumerate(patients):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(patient.name))
            if patient.date_of_birth:
                dob = patient.date_of_birth
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                age = ""
            table.setItem(i, 2, QTableWidgetItem(str(age)))
            table.setItem(i, 3, QTableWidgetItem(patient.gender))
            table.setItem(i, 4, QTableWidgetItem(patient.phone))
            # Edit button: Moves patient data to edit page.
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, p=patient: self.editor.load_patient_data(p))
            table.setCellWidget(i, 5, edit_btn)
            # Delete button: The record is deleted and the table is updated.
            del_btn = QPushButton("Delete")
            del_btn.clicked.connect(lambda checked, pid=patient.id: self.delete_and_refresh(pid))
            table.setCellWidget(i, 6, del_btn)
        print("Patients loaded successfully.")

    def load_all_patients(self):
        try:
            patients = Patients.select()
            print("Total patients:", patients.count())
            self.populate_table(patients)
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"An error occurred while loading patients: {e}")

    def delete_and_refresh(self, patient_id):
        self.deleter.delete_patient(patient_id)
        self.load_all_patients()
# =====================================================================
# PatientSearch
# Search for patients using phone number and display results in table
# =====================================================================
class PatientSearchHandler:
    def __init__(self, ui, deleter, table_manager):
        self.ui = ui
        self.deleter = deleter
        self.table_manager = table_manager

    def search_patient(self):
        search_text = self.ui.lineEdit.text().strip()
        if not search_text:
            QMessageBox.warning(self.ui, "Error", "Please enter a phone number to search.")
            return

        try:
            patients = Patients.select().where(Patients.phone.contains(search_text))
            print("Patients found:", patients.count())
            self.table_manager.populate_table(patients)
            if patients.count() == 0:
                QMessageBox.information(self.ui, "Search", "No patients found with that phone number.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"An error occurred while searching: {e}")
# =====================================================================
# PatientViewHandler
# Display patient data when clicking on the "patient_btn" button
# =====================================================================
class PatientViewHandler:
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def show_patients(self):
        self.dashboard.stackedWidget.setCurrentIndex(1)
        self.dashboard.patient_manager.load_all_patients()
# =====================================================================
# PatientManager (Wrapper)
# Call functions (add, delete, edit, display, and search)
# =====================================================================
class PatientManager:
    def __init__(self, ui):
        self.ui = ui
        self.input_handler = PatientInputHandler(ui)
        self.deleter = PatientDeleter(ui)
        self.editor = PatientEditor(ui)
        self.table_manager = PatientTableManager(ui, self.deleter, self.editor)
        self.search_handler = PatientSearchHandler(ui, self.deleter, self.table_manager)

    def load_all_patients(self):
        self.table_manager.load_all_patients()

    def search_patient(self):
        self.search_handler.search_patient()
