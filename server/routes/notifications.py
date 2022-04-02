from bottle import get, jinja2_template as template

from data import navigation
from utils.user_session import validate_user_session

############################################################
@get("/notifications")
def _():
    validate_user_session(None, "/")
    return template("notifications.html", dict(currentUrl="notifications", navigation=navigation))
