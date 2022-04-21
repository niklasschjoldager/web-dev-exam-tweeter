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

    alphabet = list("abcdefghijklmnopqrstuvwzyxæøå")
    sorted_users = []
    for letter in alphabet:
        user_list = {"letter": letter, "users": []}
        for user in users:
            if user["user_name"][0].lower() == letter:
                user_list["users"].append(user)

        sorted_users.append(user_list)

    # Destructoring
    total_users, total_tweets, total_followers, total_bookmarks, total_likes = itemgetter(
        "total_users", "total_tweets", "total_followers", "total_bookmarks", "total_likes"
    )(user_stats)

    user_stats["average_followers"] = round(total_followers / total_users, 1)
    user_stats["average_tweets"] = round(total_tweets / total_users, 1)
    user_stats["average_bookmarks"] = round(total_bookmarks / total_users, 1)
    user_stats["average_likes"] = round(total_likes / total_users, 1)

    print(user_stats)

    return template(
        "admin.html",
        dict(
            currentUrl="admin",
            mobile_navigation=mobile_navigation,
            navigation=navigation,
            navigation_dropdown=navigation_dropdown,
            logged_in_user=logged_in_user,
            users=users,
            user_stats=user_stats,
        ),
    )
