from bottle import redirect, response, request

import jwt
import mysql.connector

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET


def validate_user_session(successUrl=None, errorUrl=None):

    if not request.get_cookie("user_session"):
        if errorUrl:
            return redirect(errorUrl)
        else:
            return

    try:
        encoded_user_session = request.get_cookie("user_session", secret=JSON_WEB_TOKEN_SECRET)
        jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_user_session = f"""
            SELECT *
            FROM user_sessions
            WHERE user_session_id = %(user_session_id)s
        """

        cursor.execute(query_user_session, {"user_session_id": jwt_decoded["user_session_id"]})
        is_user_session_valid = cursor.fetchone()

        if is_user_session_valid and is_user_session_valid["user_session_id"] == jwt_decoded["user_session_id"]:
            if successUrl:
                return redirect(successUrl)
            else:
                return

        response.delete_cookie("user_session")
        if errorUrl:
            return redirect(errorUrl)
        else:
            return
    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.delete_cookie("user_session")
        if errorUrl:
            return redirect(errorUrl)
        else:
            return


def get_logged_in_user():
    try:
        if not request.get_cookie("user_session", secret=JSON_WEB_TOKEN_SECRET):
            return None

        user_session_cookie = request.get_cookie("user_session", secret=JSON_WEB_TOKEN_SECRET)
        decoded_user_session = jwt.decode(user_session_cookie, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = decoded_user_session["user_session_fk_user_id"]

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_user_data = f"""
            SELECT
                users.user_id AS id,
                users.user_username AS username,
                users.user_name AS name,
                users.user_email AS email,
                users.user_created_at AS created_at,
                users.user_bio AS bio,
                users.user_website AS website,
                users.user_location AS location,
                users.user_profile_image AS profile_image,
                users.user_cover_image AS cover_image,
                users.fk_user_roles_id AS role_id,
                (SELECT COUNT(*) FROM followers WHERE followers.fk_user_from_id = %(user_id)s) AS following,
                (SELECT COUNT(*) FROM followers WHERE followers.fk_user_to_id = %(user_id)s) AS followers
            FROM users

            WHERE users.user_id = %(user_id)s
        """

        cursor.execute(query_user_data, {"user_id": user_id})
        logged_in_user = cursor.fetchone()

        cursor.close()
        connection.close()

        return logged_in_user

    except Exception as ex:
        print(ex)
        return None
