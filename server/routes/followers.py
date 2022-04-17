from bottle import get, request, response, jinja2_template as template
from datetime import datetime
import jwt
import mysql.connector

from data import mobile_navigation, navigation, navigation_dropdown
from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/users/<user_username>/followers")
def _(user_username):
    try:
        encoded_user_session = request.get_cookie("user_session")
        user_session = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = user_session["user_session_fk_user_id"]
        logged_in_user = {
            "id": user_id,
            "name": user_session["user_session_user_name"],
            "username": user_session["user_session_user_username"],
            "profile_image": user_session["user_session_user_profile_image"],
            "cover_image": user_session["user_session_user_cover_image"],
        }

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_profile = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_get_user_profile, {"user_username": user_username})
        user_profile = cursor.fetchone()
        user_joined = datetime.fromtimestamp(user_profile["user_created_at"]).strftime("%B %Y")
        user_profile["user_joined"] = user_joined

        cursor.close()
        connection.close()

        return template(
            "user-followers",
            dict(
                currentUrl=f"users/{user_username}",
                mobile_navigation=mobile_navigation,
                navigation=navigation,
                navigation_dropdown=navigation_dropdown,
                logged_in_user=logged_in_user,
                user_profile=user_profile,
            ),
        )
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
