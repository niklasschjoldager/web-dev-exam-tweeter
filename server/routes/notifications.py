from bottle import get, view

from utils.user_session import validate_user_session

############################################################
@get("/notifications")
@view("notifications")
def _():
    validate_user_session(None, "/")
    return
