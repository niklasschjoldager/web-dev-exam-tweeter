from bottle import get, response

############################################################
@get("/users/<user_id>")
def _(user_id):
    return user_id
