from peewee import MySQLDatabase

# Setting up a database connection
db = MySQLDatabase(
    'dbapp',
    user='root',
    password='root',
    host='127.0.0.1',
    port=3306
)
