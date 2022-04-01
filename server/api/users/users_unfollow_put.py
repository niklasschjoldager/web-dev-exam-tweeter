from bottle import put

############################################################
@put("/users/<user_id>/unfollow")
def _(user_id):
    return {"info": "Unfollowed"}
