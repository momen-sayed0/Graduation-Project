from Database import db
from models import Patients

class CRUDOperations:
    @staticmethod
    def add_patient(name, date_of_birth, gender, phone, address):
        try:
            patient = Patients.create(
                name=name, 
                date_of_birth=date_of_birth, 
                gender=gender, 
                phone=phone, 
                address=address
            )
            return {'success': True, 'message': 'Patient added successfully', 'patient_id': patient.id}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_all_patients():
        try:
            patients = Patients.select()
            return [
                {'id': p.id, 'name': p.name, 'date_of_birth': p.date_of_birth, 'gender': p.gender, 'phone': p.phone, 'address': p.address}
                for p in patients
            ]
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_patient_by_id(patient_id):
        try:
            patient = Patients.get(Patients.id == patient_id)
            return {'id': patient.id, 'name': patient.name, 'date_of_birth': patient.date_of_birth, 'gender': patient.gender, 'phone': patient.phone, 'address': patient.address}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def update_patient(patient_id, name=None, date_of_birth=None, gender=None, phone=None, address=None):
        try:
            patient = Patients.get(Patients.id == patient_id)
            if name:
                patient.name = name
            if date_of_birth:
                patient.date_of_birth = date_of_birth
            if gender:
                patient.gender = gender
            if phone:
                patient.phone = phone
            if address:
                patient.address = address
            patient.save()
            return {'success': True, 'message': 'Patient updated successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def delete_patient(patient_id):
        try:
            patient = Patients.get(Patients.id == patient_id)
            patient.delete_instance()
            return {'success': True, 'message': 'Patient deleted successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
