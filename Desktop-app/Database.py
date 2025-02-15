from peewee import MySQLDatabase
import logging

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up a database connection
db = MySQLDatabase(
    'dbapp',
    user='root',
    password='root',
    host='localhost',
    port=3306,
)

try:
    db.connect()
    logger.info(" successful connection to the database")
except Exception as e:
    logger.error(f"failed to connect to the database: {e}")
    db.close()