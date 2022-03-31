from bottle import delete, response, request
import jwt
import mysql.connector
import re

from utils.user_session import validate_user_session
from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@delete("/tweets/<tweet_id>")
def _(tweet_id):
    validate_user_session()

    encoded_user_session = request.get_cookie("user_session")
    user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

    try:
        tweet_id = int(tweet_id)
        # Validate tweet ID
        if not tweet_id:
            response.status = 400
            return {"info": "Tweet ID is missing"}

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        # Delete the tweet
        query_delete_tweet = f"""
            DELETE FROM tweets
            WHERE tweet_id = %(tweet_id)s AND tweet_fk_user_id = %(user_id)s
        """

        cursor.execute(query_delete_tweet, {"tweet_id": tweet_id, "user_id": user_session["user_session_fk_user_id"]})
        connection.commit()
        is_tweet_deleted = cursor.rowcount

        if not is_tweet_deleted:
            response.status = 400
            return {"info": "Tweet not found"}

        # If tweet not found, send a 400 (Correct one: 204)
        response.status = 200
        return {"info": "Tweet successfully deleted"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
