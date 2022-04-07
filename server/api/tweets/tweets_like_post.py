from bottle import post, request, response
import jwt
import mysql.connector
import time

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

###########################################################
@post("/tweets/<tweet_id:int>/like")
def _(tweet_id):
    try:
        # Validate
        validate_user_session()

        # Who likes it? The user who is logged in
        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        user_id = user_session["user_session_fk_user_id"]

        print(user_id)

        # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_like_tweet = f"""
            INSERT INTO likes (fk_tweet_id, fk_user_id, like_created_at)
            VALUES (%s, %s, %s)
        """

        like_tweet = {"fk_tweet_id": tweet_id, "fk_user_id": user_id, "like_created_at": int(time.time())}

        cursor.execute(query_like_tweet, tuple(like_tweet.values()))
        connection.commit()

        # Update / insert the liked tweet
        response.status = 201
        return {"info": f"Tweet with id {tweet_id} liked"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
