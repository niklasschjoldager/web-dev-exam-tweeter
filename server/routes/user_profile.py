from bottle import get, request, response, jinja2_template as template
import jwt
import mysql.connector

from data import navigation
from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/users/<user_username:path>")
def _(user_username):
    try:
        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = user_session["user_session_fk_user_id"]
        logged_in_user = {
            "id": user_id,
            "name": user_session["user_session_user_name"],
            "username": user_session["user_session_user_username"],
        }

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_get_user, {"user_username": user_username})
        user_profile = cursor.fetchone()

        query_get_user_tweets = f"""
            SELECT tweets.tweet_id, tweets.tweet_image_file_name, tweets.tweet_text
            FROM tweets
            WHERE tweet_fk_user_id = %(user_id)s
            ORDER BY tweet_created_at DESC
        """
        cursor.execute(query_get_user_tweets, {"user_id": user_profile["user_id"]})
        tweets = cursor.fetchall()

        print(user_profile)

        return template(
            "user-profile",
            dict(
                currentUrl=f"users/{user_username}",
                navigation=navigation,
                tweets=tweets,
                user_profile=user_profile,
                logged_in_user=logged_in_user,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
