from bottle import get, jinja2_template as template
from operator import itemgetter
import mysql.connector

from data import mobile_navigation, navigation, navigation_dropdown
from utils.user_session import DATABASE_CONFIG, get_logged_in_user, validate_user_session

############################################################
@get("/admin")
def _():
    logged_in_user = get_logged_in_user()

    connection = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query_get_users = f"""
        SELECT  
            user_id,
            user_name,
            user_username,
            user_profile_image
        FROM users
        ORDER BY user_name ASC
    """
    cursor.execute(query_get_users)
    users = cursor.fetchall()

    query_get_tweets = f"""
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

    print(logged_in_user)

    cursor.execute(query_get_tweets, {"user_id": logged_in_user["id"]})
    tweets = cursor.fetchall()

    query_get_user_stats = f"""
        SELECT
            (SELECT COUNT(*) FROM users) AS total_users,
            (SELECT COUNT(*) FROM tweets) AS total_tweets,
            (SELECT COUNT(*) FROM followers) AS total_followers,
            (SELECT COUNT(*) FROM bookmarks) AS total_bookmarks,
            (SELECT COUNT(*) FROM likes) AS total_likes
    """
    cursor.execute(query_get_user_stats)
    user_stats = cursor.fetchone()

    alphabet = list("1234567890abcdefghijklmnopqrstuvwzyxæøå")
    sorted_users = []
    for letter in alphabet:
        user_list = {"letter": letter, "users": []}
        for user in users:
            if user["user_name"][0].lower() == letter:
                user["user_tweets"] = [tweet for tweet in tweets if tweet["tweet_fk_user_id"] == user["user_id"]]
                user_list["users"].append(user)
        if len(user_list["users"]):
            sorted_users.append(user_list)

    # Destructoring
    total_users, total_tweets, total_followers, total_bookmarks, total_likes = itemgetter(
        "total_users", "total_tweets", "total_followers", "total_bookmarks", "total_likes"
    )(user_stats)

    user_stats["average_followers"] = round(total_followers / total_users, 1)
    user_stats["average_tweets"] = round(total_tweets / total_users, 1)
    user_stats["average_bookmarks"] = round(total_bookmarks / total_users, 1)
    user_stats["average_likes"] = round(total_likes / total_users, 1)

    print(sorted_users)

    return template(
        "admin.html",
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
