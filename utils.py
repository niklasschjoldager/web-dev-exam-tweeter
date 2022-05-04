from bottle import redirect, response, request
import datetime
import jwt
import time
import math
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


def format_time_since_epoch(seconds):
    current_time = int(time.time())
    seconds_since_created = current_time - seconds

    if seconds_since_created < 60:
        return f"{seconds_since_created}s"

    minutes_since_created = math.floor(seconds_since_created / 60)
    if minutes_since_created < 60:
        return f"{minutes_since_created}m"

    hours_since_created = math.floor(minutes_since_created / 60)
    if hours_since_created < 24:
        return f"{hours_since_created}h"

    year_created = datetime.datetime.fromtimestamp(seconds_since_created).strftime("%Y")
    current_year = datetime.datetime.fromtimestamp(current_time).strftime("%Y")

    if current_year == year_created:
        return datetime.datetime.fromtimestamp(seconds_since_created).strftime("%d %b")

    return datetime.datetime.fromtimestamp(seconds).strftime("%d %b, %Y")
