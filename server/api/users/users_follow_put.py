from bottle import put, request, response
import jwt
import mysql.connector
import time

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

############################################################
@put("/users/<user_to_id:int>/follow")
def _(user_to_id):

    try:
        validate_user_session()

        if user_to_id < 1:
            response.status = 400
            return {"info": "User ID is not a valid ID"}

        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        user_from_id = user_session["user_session_fk_user_id"]

        # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_follow_user = f"""
            INSERT INTO followers (fk_user_from_id, fk_user_to_id, follower_followed_at)
            VALUES (%s, %s, %s)
        """

        follow_user = {
            "fk_user_from_id": user_from_id,
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
