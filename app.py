from bottle import default_app, get, run, static_file

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

    # Routes
    import admin
    import bookmarks
    import fourOhFour
    import home
    import index
    import lists
    import logout
    import messages
    import notifications
    import search
    import user_followers
    import user_following
    import user_profile

    # Tweets
    import tweets_by_id_get
    import tweets_delete
    import tweets_get
    import tweets_like_post
    import tweets_post
    import tweets_put
    import tweets_unlike_delete

    # Users
    import users_get 
    import users_follow_put 
    import users_post 
    import users_put 
    import users_unfollow_put

    # Auth
    import login_post

    application = default_app()
except:
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
        user_followers,
        user_following,
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
    from api.users import users_get, users_follow_put, users_post, users_put, users_unfollow_put

    # Auth
    import api.auth.login_post

    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
