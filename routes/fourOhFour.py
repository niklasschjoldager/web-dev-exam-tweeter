from bottle import error, jinja2_template as template

from utils.user_session import get_logged_in_user

############################################################
@error(404)
def _(error):
    logged_in_user = get_logged_in_user()
    print(logged_in_user)

    return template("fourOhFour.html", dict(logged_in_user=logged_in_user))
