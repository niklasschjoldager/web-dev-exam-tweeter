from bottle import redirect, response, request, post
import jwt
from mysql import connector
import re
import time
import uuid

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET, REGEX_EMAIL, REGEX_PASSWORD
from utils import validate_user_session

############################################################
@post("/login")
def _():
    validate_user_session("/home")
    connection, cursor = None, None

    try:
        # Validate email
        if not request.forms.get("user_email"):
            response.status = 400
            return {"info": "Missing email"}

        user_email = request.forms.get("user_email").strip()

        if not re.match(REGEX_EMAIL, user_email):
            response.status = 400
            return {"info": "Email is not valid"}

        # Validate Password
        if not request.forms.get("user_password"):
            response.status = 400
            return {"info": "Missing password"}

        user_password = request.forms.get("user_password")

        if not re.match(REGEX_PASSWORD, user_password):
            response.status = 400
            return {"info": "Invalid password"}

        # Validate email & password with users in database
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        user = get_user_by_email(user_email, cursor)

        if not user:
            response.status = 400
            return {"info": "E-mail does not exist"}

        if user["user_password"] != user_password:
            response.status = 400
            return {"info": "Wrong password"}

        # Create user session
        user_session = {
            "user_session_id": str(uuid.uuid4()),
            "user_session_iat": int(time.time()),
            "fk_user_id": user["user_id"],
        }

        # Add user session
        post_user_session(user_session, cursor)
        connection.commit()

        encoded_jwt = jwt.encode(user_session, JSON_WEB_TOKEN_SECRET, algorithm="HS256")
        response.set_cookie("user_session", encoded_jwt, secret=JSON_WEB_TOKEN_SECRET)

        return redirect("/home")
    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()


def post_user_session(session, cursor):
    try:
        query = f"""
            INSERT INTO user_sessions (user_session_id, user_session_iat, fk_user_id) 
            VALUES (%s, %s, %s)
        """
        params = tuple(session.values())
        cursor.execute(query, params)
        return cursor.lastrowid
    except Exception as ex:
        print(ex)
        return None


def get_user_by_email(email, cursor):
    try:
        query = f"""
            SELECT *
            FROM users
            WHERE user_email = %(user_email)s
        """
        params = {"user_email": email}
        cursor.execute(query, params)
        user = cursor.fetchone()

        return user
    except Exception as ex:
        print(ex)
        return None
