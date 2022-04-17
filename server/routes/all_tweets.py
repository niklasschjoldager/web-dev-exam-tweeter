from bottle import get, request, jinja2_template as template
import jwt
import mysql.connector

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from data import mobile_navigation, navigation, navigation_dropdown

############################################################
@get("/all-tweets")
def _():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = user_session["user_session_fk_user_id"]
        logged_in_user = {
            "id": user_id,
            "name": user_session["user_session_user_name"],
            "username": user_session["user_session_user_username"],
            "profile_image": user_session["user_session_user_profile_image"],
            "cover_image": user_session["user_session_user_cover_image"],
        }

        query = f"""
            SELECT tweets.tweet_id, tweets.tweet_image_file_name, tweets.tweet_text, users.user_username, users.user_name
            FROM users, tweets
            ORDER BY tweet_created_at DESC
        """

        cursor.execute(query)

        tweets = cursor.fetchall()

        return template(
            "all-tweets.html",
            dict(
                currentUrl="all-tweets",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweets=tweets,
                logged_in_user=logged_in_user,
            ),
        )
    except mysql.connector.Error as error:
        print(error)
