from bottle import get, response, jinja2_template as template
import mysql.connector

from data import navigation
from g import DATABASE_CONFIG

############################################################
@get("/users/<user_username:path>")
def _(user_username):
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_get_user, {"user_username": user_username})
        user = cursor.fetchone()

        query_get_user_tweets = f"""
            SELECT tweets.tweet_id, tweets.tweet_image_file_name, tweets.tweet_text
            FROM tweets
            WHERE tweet_fk_user_id = %(user_id)s
            ORDER BY tweet_created_at DESC
        """
        cursor.execute(query_get_user_tweets, {"user_id": user["user_id"]})
        tweets = cursor.fetchall()

        return template(
            "user-profile",
            dict(
                currentUrl="users",
                name=user["user_name"],
                navigation=navigation,
                tweets=tweets,
                username=user_username,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
