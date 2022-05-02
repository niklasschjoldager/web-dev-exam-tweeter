from bottle import get, response, jinja2_template as template
from mysql import connector
from datetime import datetime

from data import mobile_navigation, navigation, navigation_dropdown, user_page_default_messages, user_page_tabs
from database import get_who_to_follow
from g import DATABASE_CONFIG
from utils import format_time_since_epoch, get_logged_in_user

############################################################
@get("/users/<user_username:path>/media")
def _(user_username):
    try:
        logged_in_user = get_logged_in_user()
        if logged_in_user:
            logged_in_user_id = logged_in_user.get("id")
        else:
            logged_in_user_id = None

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        user_profile = get_user_profile(user_username, cursor)
        user_info = get_user_info(user_profile["user_id"], cursor, logged_in_user_id)
        tweets = get_user_tweets_with_media(user_profile["user_id"], cursor, logged_in_user_id)
        who_to_follow = get_who_to_follow(logged_in_user_id, cursor)

        return template(
            "user-profile",
            dict(
                currentUrl=f"users/{user_username}",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweets=tweets,
                user_profile=user_profile,
                user_page_default_messages=user_page_default_messages,
                user_page_tabs=user_page_tabs,
                active_tab="media",
                user_info=user_info,
                logged_in_user=logged_in_user,
                who_to_follow=who_to_follow,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}


def get_user_profile(username, cursor):
    query = f"""
        SELECT *
        FROM users
        WHERE user_username = %(user_username)s
    """

    params = {"user_username": username}

    cursor.execute(query, params)
    user_profile = cursor.fetchone()
    user_joined = datetime.fromtimestamp(user_profile["user_created_at"]).strftime("%B %Y")
    user_profile["user_joined"] = user_joined

    return user_profile


def get_user_info(user_id, cursor, logged_in_user_id=0):
    query = f"""
        SELECT
            (SELECT COUNT(*) 
                FROM tweets 
                WHERE tweets.tweet_fk_user_id = %(user_profile_id)s) AS tweets,
            (SELECT COUNT(*) 
                FROM followers 
                WHERE followers.fk_user_to_id = %(user_profile_id)s) AS followers,
            (SELECT COUNT(*) 
                FROM followers 
                WHERE followers.fk_user_from_id = %(user_profile_id)s) AS following,
            (SELECT COUNT(*) 
                FROM followers 
                WHERE followers.fk_user_from_id = %(logged_in_user_id)s 
                AND followers.fk_user_to_id = %(user_profile_id)s) AS is_followed_by_user
    """

    params = {"user_profile_id": user_id, "logged_in_user_id": logged_in_user_id}

    cursor.execute(query, params)
    user_info = cursor.fetchone()

    return user_info


def get_user_tweets_with_media(user_id, cursor, logged_in_user_id=0):
    query = f"""
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
            users.user_profile_image,
            COUNT(is_tweet_creator_followed_by_user.fk_user_to_id) AS is_tweet_creator_followed_by_user
        FROM tweets

        LEFT JOIN likes AS likes_quantity 
            ON likes_quantity.fk_tweet_id = tweets.tweet_id
            
        LEFT JOIN likes AS is_liked_by_user 
            ON is_liked_by_user.fk_tweet_id = tweets.tweet_id 
            AND is_liked_by_user.fk_user_id = %(logged_in_user_id)s
            
        LEFT JOIN users 
            ON users.user_id = tweets.tweet_fk_user_id

        LEFT JOIN followers AS is_tweet_creator_followed_by_user
            ON is_tweet_creator_followed_by_user.fk_user_from_id = %(logged_in_user_id)s 
            AND is_tweet_creator_followed_by_user.fk_user_to_id = tweets.tweet_fk_user_id
        
        WHERE tweets.tweet_fk_user_id = %(user_profile_id)s 
        AND tweets.tweet_image_file_name IS NOT NULL

        GROUP BY tweets.tweet_id
        ORDER BY tweets.tweet_created_at 
        DESC
    """
    params = {"user_profile_id": user_id, "logged_in_user_id": logged_in_user_id}

    cursor.execute(query, params)
    tweets = cursor.fetchall()

    for index, tweet in enumerate(tweets):
        tweet_created_at = tweets[index]["tweet_created_at"]
        tweets[index]["tweet_created_at_formatted"] = format_time_since_epoch(tweet_created_at)

    return tweets