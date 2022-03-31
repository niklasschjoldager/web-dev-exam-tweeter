from bottle import get

###########################################################
@get("/tweets")
def _():
    # Validate
    # Connect to the db
    # Send the tweets data back
    return "Tweets received"
