from bottle import get, response, request, jinja2_template as template
import json
import jwt
import mysql.connector

from data import mobile_navigation, navigation, navigation_dropdown
from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

############################################################
@get("/home")
def _():
    validate_user_session(None, "/")

    encoded_user_session = request.get_cookie("user_session")
    user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
    user_id = user_session["user_session_fk_user_id"]
    logged_in_user = {
        "id": user_id,
        "name": user_session["user_session_user_name"],
        "username": user_session["user_session_user_username"],
    }

    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_tweets = f"""
            SELECT
                tweets.tweet_id,
                tweets.tweet_text,
                tweets.tweet_fk_user_id,
                tweets.tweet_created_at,
                tweets.tweet_image_file_name,
                COUNT(likes_quantity.fk_tweet_id) AS tweet_likes,
                COUNT(is_liked_by_user.fk_user_id) AS is_liked_by_user,
                users.user_username,
                users.user_name,
                COUNT(is_tweet_creator_followed_by_user.fk_user_to_id) AS is_tweet_creator_followed_by_user
            FROM tweets

            LEFT JOIN likes AS likes_quantity
                ON likes_quantity.fk_tweet_id = tweets.tweet_id

            LEFT JOIN likes AS is_liked_by_user
                ON is_liked_by_user.fk_tweet_id = tweets.tweet_id AND is_liked_by_user.fk_user_id = %(user_id)s
                
            LEFT JOIN users 
                ON users.user_id = tweets.tweet_fk_user_id
                
            LEFT JOIN followers AS is_tweet_creator_followed_by_user
                ON is_tweet_creator_followed_by_user.fk_user_from_id = %(user_id)s AND is_tweet_creator_followed_by_user.fk_user_to_id = tweets.tweet_fk_user_id

            WHERE tweets.tweet_fk_user_id = %(user_id)s OR tweets.tweet_fk_user_id IN(SELECT fk_user_to_id FROM followers WHERE fk_user_from_id = %(user_id)s)
            GROUP BY tweets.tweet_id
            ORDER BY tweets.tweet_created_at DESC
        """

        cursor.execute(query_get_user_tweets, {"user_id": user_id})
        tweets = cursor.fetchall()

        return template(
            "home",
            dict(
                currentUrl="home",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweets=tweets,
                logged_in_user=logged_in_user,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
