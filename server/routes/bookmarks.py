from bottle import get, jinja2_template as template

from data import navigation
from utils.user_session import validate_user_session

############################################################
@get("/bookmarks")
def _():
    validate_user_session(None, "/")
    return template("bookmarks.html", dict(currentUrl="bookmarks", navigation=navigation))
