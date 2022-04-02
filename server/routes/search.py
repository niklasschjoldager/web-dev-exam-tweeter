from bottle import get, jinja2_template as template

from utils.user_session import validate_user_session

############################################################
@get("/search")
def _():
    validate_user_session(None, "/")
    return template("search.html")
