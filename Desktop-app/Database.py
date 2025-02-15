from peewee import MySQLDatabase

# Setting up a database connection
db = MySQLDatabase(
    'dbapp',
    user='root',
    password='root',
    host='localhost',
    port=3306
)

try:
    db.connect()
    print(" successful connection to the database")
except Exception as e:
    print(f"failed to connect to the database: {e}")