from bottle import delete, response
from mysql import connector

from database import get_logged_in_user
from g import DATABASE_CONFIG
from utils import validate_user_session

############################################################
@delete("/tweets/<tweet_id:int>")
def _(tweet_id):
    connection, cursor = None, None

    try:
        validate_user_session()
        logged_in_user = get_logged_in_user()

        # Validate tweet ID
        if not tweet_id:
            response.status = 400
            return {"info": "Tweet ID is missing"}

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        # Connect to the db
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        if logged_in_user["role_id"] == 2:
            # Delete the tweet as an admin
            query_delete_tweet = f"""
                DELETE FROM tweets
                WHERE tweet_id = %(tweet_id)s
            """
            cursor.execute(query_delete_tweet, {"tweet_id": tweet_id})
        else:
            # Delete the tweet as normal user
            query_delete_tweet = f"""
                DELETE FROM tweets
                WHERE tweet_id = %(tweet_id)s AND tweet_fk_user_id = %(user_id)s
            """
            cursor.execute(query_delete_tweet, {"tweet_id": tweet_id, "user_id": logged_in_user["id"]})

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
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
