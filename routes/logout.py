from bottle import get, redirect, response, request
import jwt
from mysql import connector

from database import get_logged_in_user
from g import DATABASE_CONFIG

############################################################
@get("/logout")
def _():
    connection, cursor = None, None

    try:
        if not request.get_cookie("user_session"):
            return redirect("/")

        logged_in_user = get_logged_in_user()

        if not logged_in_user:
            response.delete_cookie("user_session")
            return redirect("/")

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        user_session = get_user_session(logged_in_user["id"], cursor)

        if user_session:
            delete_user_session(logged_in_user["id"], cursor)
            connection.commit()

        response.delete_cookie("user_session")
        return redirect("/")
    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.delete_cookie("user_session")
        return redirect("/")
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()


def get_user_session(logged_in_user_id, cursor):
    query = f"""
        SELECT *
        FROM user_sessions
        WHERE user_session_id = %(user_session_id)s
    """
    params = {"user_session_id": logged_in_user_id}

    cursor.execute(query, params)
    user_session = cursor.fetchone()

    return user_session


def delete_user_session(logged_in_user_id, cursor):
    query = f"""
        DELETE FROM user_sessions
        WHERE user_session_id = %(user_session_id)s
    """
    params = {"user_session_id": logged_in_user_id}
    cursor.execute(query, params)
