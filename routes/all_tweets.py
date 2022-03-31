from bottle import get, view

import mysql.connector

from g import DATABASE_CONFIG

############################################################
@get("/all-tweets")
@view("all-tweets")
def _():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = f"""
          SELECT *
          FROM tweets
        """

        cursor.execute(query)

        tweets = cursor.fetchall()

        return dict(tweets=tweets)
    except mysql.connector.Error as error:
        print(error)
