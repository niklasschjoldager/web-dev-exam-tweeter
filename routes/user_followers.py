from bottle import get, response, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_logged_in_user, get_who_to_follow, get_user_profile
from g import DATABASE_CONFIG

############################################################
@get("/users/<username>/followers")
def _(username):
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()

        if logged_in_user:
            logged_in_user_id = logged_in_user.get("id")
        else:
            logged_in_user_id = None

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        user_profile = get_user_profile(username, cursor)
        user_followers = get_user_followers(user_profile["user_id"], cursor, logged_in_user_id)

        who_to_follow = get_who_to_follow(logged_in_user_id, cursor)

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


def get_user_followers(user_id, cursor, logged_in_user_id=0):
    query = f"""
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
    params = {"user_id": user_id, "logged_in_user_id": logged_in_user_id}
    cursor.execute(query, params)
    user_followers = cursor.fetchall()

    return user_followers
