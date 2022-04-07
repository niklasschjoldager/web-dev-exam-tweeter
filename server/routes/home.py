from bottle import get, response, request, jinja2_template as template

import jwt
import mysql.connector
from utils.user_session import validate_user_session

from data import navigation
from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/home")
def _():
    validate_user_session(None, "/")

    encoded_user_session = request.get_cookie("user_session")
    user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
    user_id = user_session["user_session_fk_user_id"]

    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_tweets = f"""
            SELECT tweets.tweet_id, tweets.tweet_text, tweets.tweet_fk_user_id, COUNT(likes_quantity.fk_tweet_id) AS tweet_likes, is_liked_by_user.fk_user_id AS is_liked_by_user, users.user_username, users.user_name
            FROM tweets

            LEFT JOIN likes AS likes_quantity 
                ON likes_quantity.fk_tweet_id = tweets.tweet_id
                
            LEFT JOIN likes AS is_liked_by_user 
                ON is_liked_by_user.fk_tweet_id = tweets.tweet_id AND is_liked_by_user.fk_user_id = %(user_id)s
                
            LEFT JOIN users 
                ON users.user_id = tweets.tweet_fk_user_id
                
            GROUP BY tweets.tweet_id
        """

        cursor.execute(query_get_user_tweets, {"user_id": user_id})
        tweets = cursor.fetchall()

        print(tweets)

        return template("home", dict(currentUrl="home", navigation=navigation, tweets=tweets, user_id=31))
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
