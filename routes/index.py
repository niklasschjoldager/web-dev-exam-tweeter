from bottle import get, view, redirect, response, request

import jwt

from utils.user_session import validate_user_session
from data import current_year, months, footer_links
from g import JSON_WEB_TOKEN_SECRET

############################################################
@get("/")
@view("index")
def _():
    validate_user_session("/home", None)

    return dict(current_year=current_year, months=months, footer_links=footer_links)
