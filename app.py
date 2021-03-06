from bottle import default_app, get, run, static_file

# Routes
from routes import (
    admin,
    bookmarks,
    fourOhFour,
    home,
    index,
    lists,
    logout,
    messages,
    notifications,
    search,
    user_tweet,
    user_followers,
    user_following,
    user_likes,
    user_media,
    user_profile,
)

# Tweets
from api.tweets import (
    tweets_by_id_get,
    tweets_delete,
    tweets_get,
    tweets_like_post,
    tweets_post,
    tweets_put,
    tweets_unlike_delete,
)

# Users
from api.users import users_follow_put, users_post, users_put, users_unfollow_put

# Auth
import api.auth.login_post

############################################################
@get("/static/<file_path:path>")
def _(file_path):
    return static_file(file_path, root="./client/static")


############################################################
@get("/tweets/<file_path:path>")
def _(file_path):
    return static_file(file_path, root="./tweets")


############################################################
@get("/js/<file_name:path>")
def _(file_name):
    return static_file(file_name, root="./client/js")


############################################################
@get("/css/<file_name:path>")
def _(file_name):
    return static_file(file_name, root="./client/css")


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
