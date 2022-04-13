from bottle import delete, request, response
import jwt
import mysql.connector
import time

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

############################################################
@delete("/users/<user_to_id:int>/unfollow")
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

        query_unfollow_user = f"""
            DELETE FROM followers
            WHERE fk_user_from_id = %(fk_user_from_id)s AND fk_user_to_id = %(fk_user_to_id)s
        """

        unfollow_user = {
            "fk_user_from_id": user_from_id,
            "fk_user_to_id": user_to_id,
        }

        cursor.execute(query_unfollow_user, unfollow_user)

        connection.commit()

        response.status = 200
        return {"info": "Unfollowed user with ID"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Oops, something went wrong"}
