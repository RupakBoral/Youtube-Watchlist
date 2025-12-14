import logging
import uvicorn
from fastapi import FastAPI, Request, Response
from app.connectDB import connectDB, get_connection, get_cursor
from app.utils import get_all_user, get_all_watchlist_info, get_my_watchlist, get_user, create_user, create_my_watchlist
from app.models import UserDetails, WatchlistDetails

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "Hello World"}

@app.get('/user/get-all')
def get_all_user_info():
    """
    Get all the user info
    """
    try:
        res = get_all_user()
        return res
    except Exception as ex:
        return {"message": f"Error getting users {ex}"}

@app.get('/user/{user_name}')
def get_user_info(user_name: str, response: Response):
    """
    Return the user details
    """
    try:
        res = get_user(user_name)
        name = res[1] or "No user name"
        id = res[0] or "No user id"
        response.set_cookie(
            key="user_id",
            value=str(id),
            samesite="lax",      
            secure=False
        )
        return {"message": "Successfully fetched", "data": res}
    except (IndexError, TypeError) as ex:
        logger.info(f"No user with the user name found: {ex}")
        return {"message": "No user with the user name found"}
    except Exception as ex:
        logger.info(f"Error in getting user: {ex}")
        return {"message": "Error occured"}

@app.post('/user/create-user')
def create_user_info(payload: UserDetails):
    """
    Create a user in user info
    """
    try:
        res = create_user(payload)
        return {"message": "Successfully Created", "data": res}
    except Exception as ex:
        return {"status": "Error", "Error": ex}

@app.get('/watchlist/get-all')
def get_all_watchlist():
    """
    Return all watchlists
    """
    try:
        res = get_all_watchlist_info()
        return {"message": "Successfully fetched", "data": res} or "No watchlist found"
    except Exception as ex:
        return "Error fetching the watchlist"

@app.get('/watchlist/get-watchlist')
def get_user_watchlist(request: Request):
    """
    Return the watchlist of the user
    """
    try:
        user_id = request.cookies['user_id']
        res = get_my_watchlist(user_id)
        return {"message": "Successfully fetched", "data": res}
    except Exception as ex:
        return f"Erorr: {ex}"

@app.post('/watchlist/create-watchlist')
def create_watchlist(watchlistDetails: WatchlistDetails, request: Request):
    try:
        user_id = request.cookies['user_id']
        res = create_my_watchlist(user_id, watchlistDetails)
        return {"message": res}
    except Exception as ex:
        return f"Erorr adding watchlist: {ex}"

@app.get('/logout')
def logout(response: Response):
    try:
        response.delete_cookie("user_id")
        return "Logged Out"
    except Exception as ex:
        return f"Error: {ex}"



if __name__ == "__main__":
    try:
        logger.info("Starting server on port 8000...")
        if connectDB():
            cur = get_cursor()
            conn = get_connection()
            uvicorn.run("main:app", host="127.0.0.1", port=3000)
        else:
            logger.error("Failed to connect to database")
    except Exception as e:
        logging.info(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()