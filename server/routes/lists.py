from bottle import get, jinja2_template as template

from data import navigation
from utils.user_session import validate_user_session

############################################################
@get("/lists")
def _():
    validate_user_session(None, "/")
    return template("lists.html", dict(currentUrl="lists", navigation=navigation))
