import logging
from peewee import MySQLDatabase

#== logging ==#
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

#== database connection ==#
db = MySQLDatabase(
    'dbapp',
    user='root',
    password='root',
    host='127.0.0.1',
    port=3306
)

class DatabaseConnection:
    def __init__(self):
        logger.info("🔄 DatabaseConnection initialized...")
        self.db = db  #== use of the unified object ==#
        logger.info("✅ Database object created successfully!")

    def connect(self):
        logger.info("🔄 Trying to connect to the database...")
        try:
            if self.db.is_closed():
                self.db.connect()
                logger.info("✅ Connected to the database (Peewee)!")
            else:
                logger.info("ℹ️ Already connected to the database (Peewee).")
        except Exception as e:
            logger.error(f"❌ Error connecting to the database: {e}")

    def close(self):
        logger.info("🔄 Attempting to close the database connection...")
        try:
            if not self.db.is_closed():
                self.db.close()
                logger.info("🔴 Database connection closed.")
            else:
                logger.info("ℹ️ No open connection to close.")
        except Exception as e:
            logger.error(f"❌ Error closing the database connection: {e}")
