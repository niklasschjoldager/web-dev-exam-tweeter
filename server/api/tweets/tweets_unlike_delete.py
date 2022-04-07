from bottle import delete, request, response
import jwt
import mysql.connector

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

############################################################
@delete("/tweets/<tweet_id:int>/unlike")
def _(tweet_id):
    try:
        # Validate
        validate_user_session()

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        # Who likes it? The user who is logged in
        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        user_id = user_session["user_session_fk_user_id"]

        # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_unlike_tweet = f"""
            DELETE FROM likes
            WHERE fk_tweet_id = %(tweet_id)s AND fk_user_id = %(user_id)s
        """

        cursor.execute(query_unlike_tweet, {"user_id": user_id, "tweet_id": tweet_id})
        connection.commit()

        response.status = 200
        return {"info": f"Tweet with id {tweet_id} unliked"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
