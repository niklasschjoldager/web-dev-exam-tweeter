from bottle import get, response, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown, user_page_default_messages, user_page_tabs
from database import get_logged_in_user, get_user_profile, get_who_to_follow
from g import DATABASE_CONFIG
from utils import format_time_since_epoch

############################################################
@get("/users/<user_username:path>")
def _(user_username):
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()
        if logged_in_user:
            logged_in_user_id = logged_in_user.get("id")
        else:
            logged_in_user_id = None

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        user_profile = get_user_profile(user_username, cursor, logged_in_user_id=logged_in_user_id)

        if not user_profile:
            response.status = 404
            return template("fourOhFour", dict(logged_in_user=logged_in_user))

        tweets = get_user_tweets(user_profile["user_id"], cursor, logged_in_user_id)
        who_to_follow = get_who_to_follow(logged_in_user_id, cursor)

        return template(
            "user-profile",
            dict(
                currentUrl=f"users/{user_username}",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweets=tweets,
                user_profile=user_profile,
                user_page_default_messages=user_page_default_messages,
                user_page_tabs=user_page_tabs,
                active_tab="",
                logged_in_user=logged_in_user,
                who_to_follow=who_to_follow,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()


def get_user_tweets(user_id, cursor, logged_in_user_id=0):
    cursor.callproc("get_user_tweets_by_id", [user_id, logged_in_user_id])
    tweets = None

    for result in cursor.stored_results():
        tweets = result.fetchall()

    if tweets:
        for index, tweet in enumerate(tweets):
            tweet_created_at = tweets[index]["tweet_created_at"]
            tweets[index]["tweet_created_at_formatted"] = format_time_since_epoch(tweet_created_at)

    return tweets
