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
        encoded_user_session = request.get_cookie("user_session")
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
        user_session_cookie = request.get_cookie("user_session")
        decoded_user_session = jwt.decode(user_session_cookie, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
        user_id = decoded_user_session["user_session_fk_user_id"]

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_user_data = f"""
            SELECT 
                user_id AS id,
                user_username AS username,
                user_name AS name,
                user_email AS email,
                user_created_at AS created_at,
                user_bio AS bio,
                user_website AS website,
                user_location AS location,
                user_profile_image AS profile_image,
                user_cover_image AS cover_image
            FROM users
            WHERE user_id = %(user_id)s
        """

        cursor.execute(query_user_data, {"user_id": user_id})
        logged_in_user = cursor.fetchone()

        return logged_in_user

    except Exception as ex:
        print(ex)
        return {"info": "Ups, something went wrong"}
