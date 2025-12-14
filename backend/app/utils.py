from datetime import date
import logging
from app.connectDB import get_connection, get_cursor
logger = logging.getLogger(__name__)


def cur_not_found():
    logger.error("Database cursor is not available")
    return None

def conn_not_found():
    logger.error("Database Connection is not available")
    return None

def get_all_user():
    """
    Get all the users
    """
    try:
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return
        
        query = "SELECT * FROM user_info"
        cur.execute(query)
        res = cur.fetchall()
        return res
    except Exception as ex:
        logger.info(f"Error: {ex}")

def get_user(user_name: str):
    """
    Get the user from the user name (QUERY)
    """
    try:
        
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return
            
        query = 'SELECT * FROM user_info WHERE user_name = %s'
        data = (user_name,)
        cur.execute(query, data)
        res = cur.fetchone()
        return res

    except Exception as ex:
        logger.info(f"Error: {ex}")
        

def create_user(userDetails):
    """
    Create a user (QUERY)
    """
    try:
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return

        user_name = userDetails.user_name or None
        name = userDetails.name or None

        if user_name is None or name is None:
            return "No user name or name"

        query = 'INSERT INTO user_info (user_name, name) VALUES (%s, %s)'
        data = (user_name, name, )
        cur.execute(query, data)

        conn = get_connection() or None
        if conn is None:
            conn_not_found()
            return
        
        conn.commit()
        return "User created succesfully"

    except Exception as ex:
        logger.info(f"Error: {ex}")

def get_all_watchlist_info():
    """
    Returns entire watchlists
    """
    try:
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return
        
        query = "SELECT * FROM watchlist"
        cur.execute(query)
        res = cur.fetchall()
        return res

    except Exception as ex:
        logger.info("Error fetching watchlist")

def get_my_watchlist(user_id):
    """
    Return user's watchlist
    """
    try:
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return
        
        query = "SELECT * FROM watchlist WHERE user_id = (%s)"
        data  = (user_id, )
        cur.execute(query, data)
        res = cur.fetchall()
        return res

    except Exception as ex:
        logger.info("Error fetching watchlist")

def create_my_watchlist(user_id, watchlistDetails):
    """
    Create a user's watchlist
    """
    try:
        cur = get_cursor() or None
        if cur is None:
            cur_not_found()
            return
        
        title = watchlistDetails.title
        url = watchlistDetails.url
        deadline = watchlistDetails.deadline

        if deadline < date.today():
            return "Error: Deadline cannot be in past"

        query = "INSERT INTO watchlist (user_id, title, url, deadline) VALUES (%s, %s, %s, %s)"
        data  = (user_id, title, url, deadline, )
        cur.execute(query, data)

        conn = get_connection() or None
        if conn is None:
            conn_not_found()
            return

        conn.commit()
        return "Watchlist added successfully"

    except Exception as ex:
        return "Error adding watchlist"