from bottle import get, response, jinja2_template as template
from datetime import datetime
import mysql.connector

from data import mobile_navigation, navigation, navigation_dropdown
from g import DATABASE_CONFIG
from utils.user_session import get_logged_in_user

############################################################
@get("/users/<user_username>/following")
def _(user_username):
    try:
        logged_in_user = get_logged_in_user()

        connection = mysql.connector.connect(**DATABASE_CONFIG)
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
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
