from bottle import get, response, jinja2_template as template
from mysql import connector

from data import mobile_navigation, navigation, navigation_dropdown
from database import get_logged_in_user, get_who_to_follow
from g import DATABASE_CONFIG

############################################################
@get("/users/<username:path>/status/<tweet_id:int>")
def _(username, tweet_id):
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()
        if logged_in_user:
            logged_in_user_id = logged_in_user.get("id")
        else:
            logged_in_user_id = None

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        tweet = get_tweet(username, tweet_id, cursor, logged_in_user_id)
        who_to_follow = get_who_to_follow(logged_in_user_id, cursor)

        if not tweet:
            response.status = 404
            return template("fourOhFour", dict(logged_in_user=logged_in_user))

        print(tweet)

        return template(
            "user-tweet",
            dict(
                logged_in_user=logged_in_user,
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                tweet=tweet,
                who_to_follow=who_to_follow,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}


def get_tweet(username, tweet_id, cursor, logged_in_user_id=0):
    query = f"""
        SELECT 
            tweets.tweet_id, 
            tweets.tweet_text, 
            tweets.fk_user_id, 
            tweets.tweet_created_at, 
            tweets.tweet_image_file_name,
            tweets.tweet_total_likes, 
            users.user_username, 
            users.user_name,
            users.user_profile_image,
            COUNT(is_tweet_creator_followed_by_user.fk_user_to_id) AS is_tweet_creator_followed_by_user,
            COUNT(is_liked_by_user.fk_user_id) AS is_liked_by_user
        FROM tweets

        LEFT JOIN users
        ON users.user_username = %(username)s

        LEFT JOIN likes AS is_liked_by_user 
            ON is_liked_by_user.fk_tweet_id = %(tweet_id)s
            AND is_liked_by_user.fk_user_id = %(logged_in_user_id)s

        LEFT JOIN followers AS is_tweet_creator_followed_by_user
            ON is_tweet_creator_followed_by_user.fk_user_from_id = %(logged_in_user_id)s 
            AND is_tweet_creator_followed_by_user.fk_user_to_id = tweets.fk_user_id

        WHERE tweets.tweet_id = %(tweet_id)s
        AND tweets.fk_user_id = users.user_id
    """
    params = {"logged_in_user_id": logged_in_user_id, "username": username, "tweet_id": tweet_id}

    cursor.execute(query, params)
    tweet = cursor.fetchone()
    return tweet
