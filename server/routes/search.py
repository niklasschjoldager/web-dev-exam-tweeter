from bottle import get, request, jinja2_template as template
import jwt

from data import navigation
from g import JSON_WEB_TOKEN_SECRET
from utils.user_session import validate_user_session

############################################################
@get("/search")
def _():
    validate_user_session(None, "/")

    encoded_user_session = request.get_cookie("user_session")
    user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
    user_id = user_session["user_session_fk_user_id"]
    logged_in_user = {
        "id": user_id,
        "name": user_session["user_session_user_name"],
        "username": user_session["user_session_user_username"],
    }

    return template("search.html", dict(currentUrl="search", navigation=navigation, logged_in_user=logged_in_user))
