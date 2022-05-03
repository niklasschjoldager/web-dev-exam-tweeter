from bottle import get, response, jinja2_template as template
from datetime import datetime
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_who_to_follow
from g import DATABASE_CONFIG
from utils import get_logged_in_user

############################################################
@get("/users/<username>/followers")
def _(username):
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_profile = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_get_user_profile, {"user_username": username})
        user_profile = cursor.fetchone()
        user_joined = datetime.fromtimestamp(user_profile["user_created_at"]).strftime("%B %Y")
        user_profile["user_joined"] = user_joined

        query_get_user_followers = f"""
            SELECT
                users.user_id,
                users.user_name,
                users.user_username,
                users.user_profile_image,
                COUNT(is_followed_by_logged_in_user.fk_user_to_id) AS is_followed_by_logged_in_user
            FROM users

            LEFT JOIN followers
                ON followers.fk_user_from_id = users.user_id
                
            LEFT JOIN followers AS is_followed_by_logged_in_user
                ON is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id

            WHERE users.user_id = followers.fk_user_from_id AND followers.fk_user_to_id = %(user_id)s
            GROUP BY users.user_id
        """
        params = {"user_id": user_profile["user_id"], "logged_in_user_id": logged_in_user["id"]}
        cursor.execute(query_get_user_followers, params)
        user_followers = cursor.fetchall()

        who_to_follow = get_who_to_follow(logged_in_user["id"], cursor)

        return template(
            "user-followers",
            dict(
                currentUrl=f"users/{username}",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                logged_in_user=logged_in_user,
                user_followers=user_followers,
                user_profile=user_profile,
                who_to_follow=who_to_follow,
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
