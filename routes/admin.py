from bottle import get, response, jinja2_template as template
from operator import itemgetter
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_logged_in_user
from g import DATABASE_CONFIG

############################################################
@get("/admin")
def _():
    connection, cursor, logged_in_user_id = None, None, None

    try:
        logged_in_user = get_logged_in_user()

        if logged_in_user:
            logged_in_user_id = logged_in_user["id"]

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        users = get_all_users(cursor)
        tweets = get_all_tweets(cursor, logged_in_user_id)
        user_stats = get_all_user_stats(cursor)
        sorted_users = []

        if users:
            alphabet = list("1234567890abcdefghijklmnopqrstuvwzyxæøå")
            for letter in alphabet:
                user_list = {"letter": letter, "users": []}
                for user in users:
                    if user["user_name"][0].lower() == letter:
                        if tweets:
                            user["user_tweets"] = [tweet for tweet in tweets if tweet["fk_user_id"] == user["user_id"]]
                        user_list["users"].append(user)
                if len(user_list["users"]):
                    sorted_users.append(user_list)

        if user_stats:
            # Destructoring
            total_users, total_tweets, total_followers, total_bookmarks, total_likes = itemgetter(
                "total_users", "total_tweets", "total_followers", "total_bookmarks", "total_likes"
            )(user_stats)

            user_stats["average_followers"] = round(total_followers / total_users, 1)
            user_stats["average_tweets"] = round(total_tweets / total_users, 1)
            user_stats["average_bookmarks"] = round(total_bookmarks / total_users, 1)
            user_stats["average_likes"] = round(total_likes / total_users, 1)

        return template(
            "admin",
            dict(
                currentUrl="admin",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                logged_in_user=logged_in_user,
                users=sorted_users,
                user_stats=user_stats,
                tweets=tweets,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()


def get_all_tweets(cursor, logged_in_user_id=0):
    try:
        query = f"""
            SELECT
                tweets.tweet_id,
                tweets.tweet_text,
                tweets.fk_user_id,
                tweets.tweet_created_at,
                tweets.tweet_image_file_name,
                tweets.tweet_total_likes,
                COUNT(is_liked_by_user.fk_user_id) AS is_liked_by_user,
                users.user_username,
                users.user_name,
                users.user_profile_image,
                COUNT(is_tweet_creator_followed_by_user.fk_user_to_id) AS is_tweet_creator_followed_by_user
            FROM tweets

            LEFT JOIN users 
                ON users.user_id = tweets.fk_user_id

            LEFT JOIN likes AS is_liked_by_user
                ON is_liked_by_user.fk_tweet_id = tweets.tweet_id 
                AND is_liked_by_user.fk_user_id = %(user_id)s
                
            LEFT JOIN followers AS is_tweet_creator_followed_by_user
                ON is_tweet_creator_followed_by_user.fk_user_from_id = %(user_id)s 
                AND is_tweet_creator_followed_by_user.fk_user_to_id = tweets.fk_user_id

            GROUP BY tweets.tweet_id
            ORDER BY tweets.tweet_created_at DESC
        """
        params = {"user_id": logged_in_user_id}

        cursor.execute(query, params)
        tweets = cursor.fetchall()
        return tweets
    except Exception as ex:
        print(ex)
        return None


def get_all_user_stats(cursor):
    try:
        query = f"""
                SELECT
                    (SELECT COUNT(*) FROM users) AS total_users,
                    (SELECT COUNT(*) FROM tweets) AS total_tweets,
                    (SELECT COUNT(*) FROM followers) AS total_followers,
                    (SELECT COUNT(*) FROM bookmarks) AS total_bookmarks,
                    (SELECT COUNT(*) FROM likes) AS total_likes
            """
        cursor.execute(query)
        user_stats = cursor.fetchone()

        return user_stats
    except Exception as ex:
        print(ex)
        return None


def get_all_users(cursor):
    try:
        query = f"""
            SELECT  
                user_id,
                user_name,
                user_username,
                user_profile_image
            FROM users
            ORDER BY user_name ASC
        """
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except Exception as ex:
        print(ex)
        return None
