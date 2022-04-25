from bottle import get, response, jinja2_template as template
import mysql.connector

from data import mobile_navigation, navigation, navigation_dropdown
from g import DATABASE_CONFIG
from utils.user_session import get_logged_in_user, validate_user_session

############################################################
@get("/home")
def _():
    validate_user_session(None, "/")
    logged_in_user = get_logged_in_user()

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
                users.user_profile_image,
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

        cursor.execute(query_get_user_tweets, {"user_id": logged_in_user["id"]})
        tweets = cursor.fetchall()


        query_get_user_followers = f"""
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

        cursor.execute(query_get_user_followers, {"logged_in_user_id": logged_in_user["id"]})
        who_to_follow = cursor.fetchall()

        return template(
            "home",
            dict(
                currentUrl="home",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweets=tweets,
                logged_in_user=logged_in_user,
                who_to_follow=who_to_follow
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
