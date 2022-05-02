from bottle import get, response, jinja2_template as template
from datetime import datetime
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_who_to_follow
from g import DATABASE_CONFIG
from utils import get_logged_in_user

############################################################
@get("/users/<user_username>/following")
def _(user_username):
    try:
        logged_in_user = get_logged_in_user()

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_profile = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_get_user_profile, {"user_username": user_username})
        user_profile = cursor.fetchone()
        user_joined = datetime.fromtimestamp(user_profile["user_created_at"]).strftime("%B %Y")
        user_profile["user_joined"] = user_joined

        query_get_user_following = f"""
            SELECT
                users.user_id,
                users.user_name,
                users.user_username,
                users.user_profile_image,
                COUNT(is_followed_by_logged_in_user.fk_user_to_id) AS is_followed_by_logged_in_user
            FROM users

            LEFT JOIN followers
                ON followers.fk_user_from_id = %(user_id)s
                
            LEFT JOIN followers AS is_followed_by_logged_in_user
                ON is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id

            WHERE users.user_id = followers.fk_user_to_id
            GROUP BY users.user_id
        """

        cursor.execute(
            query_get_user_following, {"user_id": user_profile["user_id"], "logged_in_user_id": logged_in_user["id"]}
        )

        user_following = cursor.fetchall()

        who_to_follow = get_who_to_follow(logged_in_user["id"], cursor)

        cursor.close()
        connection.close()

        return template(
            "user-following",
            dict(
                currentUrl=f"users/{user_username}",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                logged_in_user=logged_in_user,
                user_profile=user_profile,
                user_following=user_following,
                who_to_follow=who_to_follow,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
