from bottle import get, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_who_to_follow
from g import DATABASE_CONFIG
from utils import get_logged_in_user, validate_user_session

############################################################
@get("/search")
def _():
    validate_user_session(None, "/")
    logged_in_user = get_logged_in_user()
    who_to_follow = None

    if logged_in_user:
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        who_to_follow = get_who_to_follow(logged_in_user["id"], cursor)

    return template(
        "search",
        dict(
            currentUrl="search",
            mobile_navigation=mobile_navigation,
            navigation=navigation,
            navigation_dropdown=navigation_dropdown,
            logged_in_user=logged_in_user,
            who_to_follow=who_to_follow,
        ),
    )
