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

        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_user_session = f"""
            SELECT *
            FROM user_sessions
            WHERE user_session_id = %(user_session_id)s
        """

        cursor.execute(query_user_session, {"user_session_id": logged_in_user["id"]})
        user_session_in_database = cursor.fetchone()

        if user_session_in_database:
            query_delete_user_session = f"""
                DELETE FROM user_sessions
                WHERE user_session_id = %(user_session_id)s
            """
            cursor.execute(query_delete_user_session, {"user_session_id": logged_in_user["id"]})
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
