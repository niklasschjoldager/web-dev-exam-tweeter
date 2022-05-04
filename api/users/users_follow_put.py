from bottle import put, response
from mysql import connector
import time

from database import get_logged_in_user
from g import DATABASE_CONFIG
from utils import validate_user_session

############################################################
@put("/users/<user_to_id:int>/follow")
def _(user_to_id):
    validate_user_session()
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()

        if user_to_id < 1:
            response.status = 400
            return {"info": "User ID is not a valid ID"}

        # Connect to the db
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_follow_user = f"""
            INSERT INTO followers (fk_user_from_id, fk_user_to_id, follower_followed_at)
            VALUES (%s, %s, %s)
        """

        follow_user = {
            "fk_user_from_id": logged_in_user["id"],
            "fk_user_to_id": user_to_id,
            "follower_followed_at": int(time.time()),
        }

        cursor.execute(query_follow_user, tuple(follow_user.values()))
        connection.commit()

        response.status = 200
        return {"info": "Followed"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Oops, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
