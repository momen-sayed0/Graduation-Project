from peewee import *
from Database import db  # Import contact from Database file

# Basic model for connection control
class BaseModel(Model):
    class Meta:
        database = db

# Users table definition
class Users(BaseModel):
    UserName = CharField(unique=True)
    passwd = TextField()
    role = CharField()

# Patients table definition
class Patients(BaseModel):
    id = AutoField()
    name = CharField(max_length=50)
    date_of_birth = DateField()
    gender = CharField(max_length=10)
    phone = CharField(max_length=15)
    address = TextField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
