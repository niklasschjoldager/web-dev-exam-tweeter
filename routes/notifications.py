from bottle import get, response, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_logged_in_user, get_who_to_follow
from g import DATABASE_CONFIG
from utils import validate_user_session

############################################################
@get("/notifications")
def _():
    connection, cursor = None, None
    try:
        validate_user_session(None, "/")
        logged_in_user = get_logged_in_user()

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        who_to_follow = get_who_to_follow(logged_in_user["id"], cursor)

        return template(
            "notifications",
            dict(
                currentUrl="notifications",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                logged_in_user=logged_in_user,
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
