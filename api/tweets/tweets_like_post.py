from bottle import post, response
import mysql.connector
import time

from g import DATABASE_CONFIG
from utils import get_logged_in_user, validate_user_session

###########################################################
@post("/tweets/<tweet_id:int>/like")
def _(tweet_id):
    try:
        # Validate
        validate_user_session()

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        logged_in_user = get_logged_in_user()

        # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_like_tweet = f"""
            INSERT INTO likes (fk_tweet_id, fk_user_id, like_created_at)
            VALUES (%s, %s, %s)
        """

        like_tweet = {"fk_tweet_id": tweet_id, "fk_user_id": logged_in_user["id"], "like_created_at": int(time.time())}

        cursor.execute(query_like_tweet, tuple(like_tweet.values()))
        connection.commit()

        # Update / insert the liked tweet
        response.status = 201
        return {"info": f"Tweet with id {tweet_id} liked"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
