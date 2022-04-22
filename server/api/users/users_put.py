from bottle import put, request, response
import jwt
import imghdr
import mysql.connector
import os
import uuid
import json

from utils.user_session import validate_user_session, get_logged_in_user
from g import (
    DATABASE_CONFIG,
    IMAGE_ALLOWED_FILE_EXTENSIONS,
    USER_BIO_MAX_LENGTH,
    USER_BIO_MIN_LENGTH,
    USER_IMAGE_PATH,
    USER_LOCATION_MAX_LENGTH,
    USER_LOCATION_MIN_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_WEBSITE_MAX_LENGTH,
    USER_WEBSITE_MIN_LENGTH,
)

###########################################################
@put("/users/<user_id:int>")
def _(user_id):
    validate_user_session()
    logged_in_user = get_logged_in_user()

    try:
        if user_id < 1:
            response.status = 400
            return {"info": "User ID is not a valid ID"}

        # User ID
        if user_id != logged_in_user["id"]:
            response.status = 400
            return {"info": "Wrong user"}

        query_set_parts = ["user_id = %(user_id)s"]
        query_params = {"user_id": user_id}

        # User name
        if request.forms.get("user_name"):
            user_name = request.forms.get("user_name").strip()

            if len(user_name) < USER_NAME_MIN_LENGTH:
                response.status = 400
                return {"info": f"Name must be at least {USER_NAME_MIN_LENGTH} characters long"}

            if len(user_name) > USER_NAME_MAX_LENGTH:
                response.status = 400
                return {"info": f"Name can only have a maximum of {USER_NAME_MAX_LENGTH} characters"}

            query_set_parts.append("user_name = %(user_name)s")
            query_params["user_name"] = user_name

        # User bio
        if request.forms.get("user_bio") or request.forms.get("user_bio") is not None:
            user_bio = request.forms.get("user_bio").strip()

            if len(user_bio) < USER_BIO_MIN_LENGTH:
                response.status = 400
                return {"info": f"Bio must be a least {USER_BIO_MIN_LENGTH} character"}

            if len(user_bio) > USER_BIO_MAX_LENGTH:
                response.status = 400
                return {"info": f"User bio can only have a maximum of {USER_BIO_MAX_LENGTH} characters"}

            query_set_parts.append("user_bio = %(user_bio)s")
            query_params["user_bio"] = user_bio

        if not request.forms.get("user_bio") and request.forms.get("user_bio") is not None:
            query_set_parts.append("user_bio = %(user_bio)s")
            query_params["user_bio"] = None

        # User location
        if request.forms.get("user_location"):
            user_location = request.forms.get("user_location").strip()

            if len(user_location) < USER_LOCATION_MIN_LENGTH:
                response.status = 400
                return {"info": f"Location must be a least {USER_LOCATION_MIN_LENGTH} character"}

            if len(user_location) > USER_LOCATION_MAX_LENGTH:
                response.status = 400
                return {"info": f"User location can only have a maximum of {USER_LOCATION_MAX_LENGTH} characters"}

            query_set_parts.append("user_location = %(user_location)s")
            query_params["user_location"] = user_location

        if not request.forms.get("user_location") and request.forms.get("user_location") is not None:
            query_set_parts.append("user_location = %(user_location)s")
            query_params["user_location"] = None

        # User website
        if request.forms.get("user_website"):
            user_website = request.forms.get("user_website").strip()

            if len(user_website) < USER_WEBSITE_MIN_LENGTH:
                response.status = 400
                return {"info": f"website must be a least {USER_WEBSITE_MIN_LENGTH} character"}

            if len(user_website) > USER_WEBSITE_MAX_LENGTH:
                response.status = 400
                return {"info": f"User website can only have a maximum of {USER_WEBSITE_MAX_LENGTH} characters"}

            query_set_parts.append("user_website = %(user_website)s")
            query_params["user_website"] = user_website

        if not request.forms.get("user_website") and request.forms.get("user_website") is not None:
            query_set_parts.append("user_website = %(user_website)s")
            query_params["user_website"] = None

        # User profile image
        if request.files.get("user_profile_image"):
            image = request.files.get("user_profile_image")
            file_name, file_extension = os.path.splitext(image.filename)

            if file_extension not in IMAGE_ALLOWED_FILE_EXTENSIONS:
                response.status = 400
                return {"info": f"Profile image format not allowed"}

            # Convert old .jpg extension to .jpeg, so it passes imghdr.what validation
            if file_extension == ".jpg":
                file_extension = ".jpeg"

            image_id = str(uuid.uuid4())
            image_name = f"{image_id}{file_extension}"
            image_path = f"{USER_IMAGE_PATH}/{image_name}"

            image.save(image_path)
            validated_file_extension = imghdr.what(image_path)

            if file_extension != f".{validated_file_extension}":
                os.remove(image_path)
                response.status = 400
                return {"info": "Invalid image format"}

            query_set_parts.append("user_profile_image = %(user_profile_image)s")
            query_params["user_profile_image"] = image_name

        # User cover image
        if request.files.get("user_cover_image"):
            image = request.files.get("user_cover_image")
            file_name, file_extension = os.path.splitext(image.filename)

            if file_extension not in IMAGE_ALLOWED_FILE_EXTENSIONS:
                response.status = 400
                return {"info": f"Cover image format not allowed"}

            # Convert old .jpg extension to .jpeg, so it passes imghdr.what validation
            if file_extension == ".jpg":
                file_extension = ".jpeg"

            image_id = str(uuid.uuid4())
            image_name = f"{image_id}{file_extension}"
            image_path = f"{USER_IMAGE_PATH}/{image_name}"

            image.save(image_path)
            validated_file_extension = imghdr.what(image_path)

            if file_extension != f".{validated_file_extension}":
                os.remove(image_path)
                response.status = 400
                return {"info": "Invalid image format"}

            query_set_parts.append("user_cover_image = %(user_cover_image)s")
            query_params["user_cover_image"] = image_name

        if request.forms.get("user_cover_image") is not None:
            query_set_parts.append("user_cover_image = %(user_cover_image)s")
            query_params["user_cover_image"] = None

        query_set_parts = ",".join(query_set_parts)

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_edit_user = f"""
            UPDATE users
            SET {query_set_parts}
            WHERE user_id = %(user_id)s
        """
        cursor.execute(query_edit_user, query_params)

        connection.commit()

        print(query_set_parts)

        # Success
        response.status = 200
        return json.dumps(query_params)
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
