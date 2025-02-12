from peewee import fn
from models import Users

# User authentication using SHA-256 directly in MySQL
def verify_user(username, password ,role):
    return Users.select().where(
        (Users.UserName == username) &
        (Users.passwd == fn.UNHEX(fn.SHA2(password, 256))) &  # Using Encryption in MySQL
        (Users.role == role)
    ).exists()

