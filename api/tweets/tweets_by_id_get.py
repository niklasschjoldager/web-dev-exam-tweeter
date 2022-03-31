from bottle import get

###########################################################
@get("/tweets/<tweet_id>")
def _(tweet_id):
    # Validate
    # Connect to the db
    # Send the tweet data back
    return "Tweet received"
