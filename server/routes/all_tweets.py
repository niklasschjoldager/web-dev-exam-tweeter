from bottle import get, jinja2_template as template

import mysql.connector

from g import DATABASE_CONFIG

############################################################
@get("/all-tweets")
def _():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = f"""
            SELECT tweets.tweet_id, tweets.tweet_image_file_name, tweets.tweet_text, users.user_username, users.user_name
            FROM users, tweets
            ORDER BY tweet_created_at DESC
        """

        cursor.execute(query)

        tweets = cursor.fetchall()

        return template("all-tweets.html", dict(tweets=tweets))
    except mysql.connector.Error as error:
        print(error)
