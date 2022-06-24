from bottle import request
from datetime import datetime
import jwt
from mysql import connector

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET
from utils import format_time_since_epoch


def get_who_to_follow(logged_in_user_id, cursor):
    query = f"""
        SELECT
            users.user_id,
            users.user_name,
            users.user_username,
            users.user_profile_image,
            COUNT(is_followed_by_logged_in_user.fk_user_to_id) AS is_followed_by_logged_in_user
        FROM users
            
        LEFT JOIN followers AS is_followed_by_logged_in_user
            ON is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id

        WHERE NOT users.user_id = %(logged_in_user_id)s

        GROUP BY users.user_id
        HAVING COUNT(is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id) < 1
        LIMIT 3
    """
    params = {"logged_in_user_id": logged_in_user_id}

    cursor.execute(query, params)
    who_to_follow = cursor.fetchall()
    return who_to_follow


def get_user_profile(username, cursor, logged_in_user_id=0):
    cursor.callproc("get_user_profile_by_username", [username, logged_in_user_id])
    user_profile = None

    for result in cursor.stored_results():
        user_profile = result.fetchone()

    if user_profile:
        user_joined = datetime.fromtimestamp(user_profile["user_created_at"]).strftime("%B %Y")
        user_profile["user_joined"] = user_joined

    return user_profile


def get_user_tweets_with_media(user_id, cursor, logged_in_user_id=0):
    cursor.callproc("get_user_tweets_with_media_by_id", [user_id, logged_in_user_id])
    tweets = None

    for result in cursor.stored_results():
        tweets = result.fetchall()

    if tweets:
        for index, tweet in enumerate(tweets):
            tweet_created_at = tweets[index]["tweet_created_at"]
            tweets[index]["tweet_created_at_formatted"] = format_time_since_epoch(tweet_created_at)

    return tweets


def get_logged_in_user():
    connection, cursor = None, None

    try:
        if not request.get_cookie("user_session", secret=JSON_WEB_TOKEN_SECRET):
            return None

        user_session_cookie = request.get_cookie("user_session", secret=JSON_WEB_TOKEN_SECRET)
        decoded_user_session = jwt.decode(user_session_cookie, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = decoded_user_session["fk_user_id"]

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = f"""
            SELECT
                users.user_id AS id,
                users.user_username AS username,
                users.user_name AS name,
                users.user_email AS email,
                users.user_created_at AS created_at,
                users.user_bio AS bio,
                users.user_website AS website,
                users.user_location AS location,
                users.user_profile_image AS profile_image,
                users.user_cover_image AS cover_image,
                users.fk_user_roles_id AS role_id,
                (SELECT COUNT(*) FROM followers WHERE followers.fk_user_from_id = %(user_id)s) AS following,
                (SELECT COUNT(*) FROM followers WHERE followers.fk_user_to_id = %(user_id)s) AS followers
            FROM users

            WHERE users.user_id = %(user_id)s
        """
        params = {"user_id": user_id}

        cursor.execute(query, params)
        logged_in_user = cursor.fetchone()

        return logged_in_user

    except Exception as ex:
        print(ex)
        return None
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
