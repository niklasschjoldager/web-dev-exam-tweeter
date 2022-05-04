from bottle import delete, response
from mysql import connector

from database import get_logged_in_user
from g import DATABASE_CONFIG
from utils import validate_user_session

############################################################
@delete("/tweets/<tweet_id:int>/unlike")
def _(tweet_id):
    validate_user_session()
    connection, cursor = None, None

    try:
        # Validate
        logged_in_user = get_logged_in_user()

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        # Connect to the db
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_unlike_tweet = f"""
            DELETE FROM likes
            WHERE fk_tweet_id = %(tweet_id)s AND fk_user_id = %(user_id)s
        """

        cursor.execute(query_unlike_tweet, {"user_id": logged_in_user["id"], "tweet_id": tweet_id})
        connection.commit()

        response.status = 200
        return {"info": f"Tweet with id {tweet_id} unliked"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
