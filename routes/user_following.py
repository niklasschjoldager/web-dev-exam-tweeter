from bottle import get, response, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_logged_in_user, get_who_to_follow, get_user_profile
from g import DATABASE_CONFIG

############################################################
@get("/users/<user_username>/following")
def _(user_username):
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        user_profile = get_user_profile(user_username, cursor)
        user_following = get_user_following(user_profile["user_id"], logged_in_user["id"], cursor)
        who_to_follow = get_who_to_follow(logged_in_user["id"], cursor)

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
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()


def get_user_following(user_id, logged_in_user_id, cursor):
    query = f"""
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
    params = {"user_id": user_id, "logged_in_user_id": logged_in_user_id}
    cursor.execute(query, params)
    user_following = cursor.fetchall()

    return user_following
