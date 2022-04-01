from bottle import put

###########################################################
@put("/tweets/<tweet_id>/like")
def _(tweet_id):
    # Validate
    # Who likes it? The user who is logged in
    # Connect to the db
    # Update / insert the liked tweet
    return f"Tweet with id {tweet_id} liked"
