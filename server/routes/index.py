from bottle import get, jinja2_template as template

import jwt

from utils.user_session import validate_user_session
from data import current_year, months, footer_links
from g import JSON_WEB_TOKEN_SECRET

############################################################
@get("/")
def _():
    validate_user_session("/home", None)

    return template("index.html", dict(current_year=current_year, months=months, footer_links=footer_links))
