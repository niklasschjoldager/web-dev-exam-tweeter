from bottle import post, response, request
import jwt
from mysql import connector
import re
import time
import uuid

from g import (
    DATABASE_CONFIG,
    JSON_WEB_TOKEN_SECRET,
    REGEX_EMAIL,
    REGEX_PASSWORD,
    REGEX_USERNAME,
    USER_NAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_USERNAME_MAX_LENGTH,
    USER_USERNAME_MIN_LENGTH,
)

############################################################
@post("/users")
def _():
    connection, cursor = None, None

    try:
        ############################################################
        # Open Database
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        # Validate username
        if not request.forms.get("user_username"):
            response.status = 400
            return {"info": "Username is missing"}

        user_username = request.forms.get("user_username").strip().replace(" ", "")

        if len(user_username) < USER_USERNAME_MIN_LENGTH:
            response.status = 400
            return {"info": f"Username must be at least {USER_USERNAME_MIN_LENGTH} characters long"}

        if len(user_username) > USER_USERNAME_MAX_LENGTH:
            response.status = 400
            return {"info": f"Username can only have a maximum of {USER_USERNAME_MAX_LENGTH} characters"}

        if not re.match(REGEX_USERNAME, user_username):
            response.status = 400
            return {
                "info": "Username can only have letters from a-z (Uppercase and lowercase), numbers 0-9, underscores and hyphens"
            }

        query_username = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        cursor.execute(query_username, {"user_username": user_username})
        is_username_taken = cursor.fetchone()

        if is_username_taken:
            response.status = 400
            return {"info": "Username already exists - Forgot password?"}

        ############################################################
        # Validate email
        if not request.forms.get("user_email"):
            response.status = 400
            return {"info": "Email is missing"}

        user_email = request.forms.get("user_email").strip()

        if not re.match(REGEX_EMAIL, user_email):
            response.status = 400
            return {"info": "Email is not invalid"}

        query_email = f"""
            SELECT *
            FROM users
            WHERE user_email = %(user_email)s
        """

        cursor.execute(query_email, {"user_email": user_email})
        is_email_registered = cursor.fetchone()

        if is_email_registered:
            response.status = 400
            return {"info": "Email already exists - Forgot your password?"}

        ############################################################
        # Validate password
        if not request.forms.get("user_password"):
            response.status = 400
            return {"info": "Password is missing"}

        user_password = request.forms.get("user_password")

        if len(user_password) < USER_PASSWORD_MIN_LENGTH:
            response.status = 400
            return {"info": f"Password must be at least {USER_PASSWORD_MIN_LENGTH} characters long"}

        if not re.match(REGEX_PASSWORD, user_password):
            response.status = 400
            return {
                "info": "Password must be at least 8 characters long, have 1 uppercase letter, 1 lowercase letter and 1 number or 1 symbol"
            }

        ############################################################
        # Validate name
        if not request.forms.get("user_name"):
            response.status = 400
            return {"info": "Name is missing"}

        user_name = request.forms.get("user_name").strip()

        if len(user_name) < USER_NAME_MIN_LENGTH:
            response.status = 400
            return {"info": f"Name must be at least {USER_NAME_MIN_LENGTH} characters long"}

        if len(user_name) > USER_NAME_MAX_LENGTH:
            response.status = 400
            return {"info": f"Name can only have a maximum of {USER_NAME_MAX_LENGTH} characters"}

        ############################################################

        # Create user
        user_created_at = int(time.time())
        user = (user_username, user_name, user_email, user_password, user_created_at)

        ############################################################
        # Add user
        query_add_user = f"""
            INSERT INTO users (user_id, user_username, user_name, user_email, user_password, user_created_at, user_updated_at, user_bio, user_is_active, user_website, user_location, user_birth_date, user_profile_image, user_cover_image)
            VALUES (NULL, %s, %s, %s, %s, %s, NULL, '', '1', '', '', NULL, '', '') 
        """

        cursor.execute(query_add_user, user)
        connection.commit()

        user_id = cursor.lastrowid

        ############################################################

        add_user_session = f"""
            INSERT INTO user_sessions (user_session_id, user_session_iat, user_session_fk_user_id) 
            VALUES (%s, %s, %s)
        """

        user_session_id = str(uuid.uuid4())
        user_session_iat = int(time.time())

        # Create user session
        db_user_session = {
            "user_session_id": user_session_id,
            "user_session_iat": user_session_iat,
            "user_session_fk_user_id": user_id,
        }

        cookie_user_session = {
            "user_session_id": user_session_id,
            "user_session_iat": user_session_iat,
            "user_session_fk_user_id": user_id,
            "user_session_user_username": user_username,
            "user_session_user_name": user_name,
        }

        cursor.execute(add_user_session, tuple(db_user_session.values()))
        connection.commit()

        ############################################################
        # Success

        encoded_jwt = jwt.encode(cookie_user_session, JSON_WEB_TOKEN_SECRET, algorithm="HS256")
        response.set_cookie("user_session", encoded_jwt, secret=JSON_WEB_TOKEN_SECRET)
        response.status = 201
        return {"user_id": 12312312312}  # TODO get user id
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
