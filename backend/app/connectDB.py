import psycopg2
import logging
from app.config import settings

logger = logging.getLogger(__name__)

cur = None
conn = None

def connectDB():
    """
    Connect to the Database
    """
    global cur, conn
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=settings.psql_database,
            user=settings.psql_username,
            password=settings.psql_password,
            port=settings.psql_port
        )
        logger.info("Connected to Database successfully!!!")
        # cursor
        cur = conn.cursor()

    except Exception as e:
        logger.info(f"Error: {e}")
        return False
    return True

def get_cursor():
    """Get the current database cursor"""
    return cur

def get_connection():
    """Get the current database connection"""
    return conn