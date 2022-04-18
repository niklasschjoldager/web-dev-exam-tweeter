from bottle import get, jinja2_template as template
import mysql.connector

from g import DATABASE_CONFIG
from data import mobile_navigation, navigation, navigation_dropdown
from utils.user_session import get_logged_in_user

############################################################
@get("/all-tweets")
def _():
    try:
        logged_in_user = get_logged_in_user()

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

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
