from bottle import get, jinja2_template as template

from data import mobile_navigation, navigation, navigation_dropdown
from utils import get_logged_in_user, validate_user_session

############################################################
@get("/notifications")
def _():
    validate_user_session(None, "/")
    logged_in_user = get_logged_in_user()

    return template(
        "notifications.html",
        dict(
            currentUrl="notifications",
            mobile_navigation=mobile_navigation,
            navigation=navigation,
            navigation_dropdown=navigation_dropdown,
            logged_in_user=logged_in_user,
        ),
    )
