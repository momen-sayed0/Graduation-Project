from peewee import *
import hashlib

db =MySQLDatabase ('my_database', user='root', password='', host='127.0.0.1', port=3306,
                   charset='utf8mb4')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    role = CharField()

class Patient(BaseModel):
    name = CharField()
    age = IntegerField()
    disease = CharField()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    with db:
        db.create_tables([User, Patient])

def insert_default_users():
    users = [
        {"username": "doc", "password": hash_password("doc123"), "role": "Doctor"},
        {"username": "assist", "password": hash_password("assist123"), "role": "Assistant"}
    ]
    for user in users:
        User.get_or_create(username=user["username"], defaults=user)

def verify_user(username, password, role):
    hashed_password = hash_password(password)
    return User.select().where(
        (User.username == username) & 
        (User.password == hashed_password) & 
        (User.role == role)
    ).exists()

create_tables()
insert_default_users()
