from bottle import get, view

from utils.user_session import validate_user_session

############################################################
@get("/messages")
@view("messages")
def _():
    validate_user_session(None, "/")
    return
