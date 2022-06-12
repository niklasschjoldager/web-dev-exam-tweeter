from bottle import post, response, request
import imghdr
from mysql import connector
import os
import time
import uuid

from database import get_logged_in_user
from g import (
    DATABASE_CONFIG,
    IMAGE_ALLOWED_FILE_EXTENSIONS,
    TWEET_IMAGE_PATH,
    TWEET_TEXT_MAX_LENGTH,
    TWEET_TEXT_MIN_LENGTH,
)
from utils import validate_user_session, format_time_since_epoch

############################################################
@post("/tweets")
def _():
    validate_user_session()
    connection, cursor = None, None

    try:
        logged_in_user = get_logged_in_user()

        ############################################################
        # Validate text
        if not request.forms.get("tweet_text"):
            response.status = 400
            return {"info": "Tweet text is missing"}

        tweet_text = request.forms.get("tweet_text").strip()

        if len(tweet_text) < TWEET_TEXT_MIN_LENGTH:
            response.status = 400
            return {"info": f"Tweet must be at least {TWEET_TEXT_MIN_LENGTH} characters long"}

        if len(tweet_text) > TWEET_TEXT_MAX_LENGTH:
            response.status = 400
            return {"info": f"Tweet can only have a maximum of {TWEET_TEXT_MAX_LENGTH} characters"}

        ############################################################
        # Validate media (image / video)
        image_url = None

        if request.files.get("tweet_image"):
            image = request.files.get("tweet_image")
            file_name, file_extension = os.path.splitext(image.filename)

            if file_extension not in IMAGE_ALLOWED_FILE_EXTENSIONS:
                response.status = 400
                return {"info": f"Image format not allowed"}

            # Convert old .jpg extension to .jpeg, so it passes imghdr.what validation
            if file_extension == ".jpg":
                file_extension = ".jpeg"

            image_id = str(uuid.uuid4())
            image_name = f"{image_id}{file_extension}"
            image_path = f"{TWEET_IMAGE_PATH}/{image_name}"

            image.save(image_path)
            validated_file_extension = imghdr.what(image_path)

            if file_extension != f".{validated_file_extension}":
                os.remove(image_path)
                response.status = 400
                return {"info": "Invalid image format"}

            image_url = image_name

        ############################################################
        # Create tweet
        tweet_created_at = int(time.time())

        db_tweet = {
            "fk_user_id": logged_in_user["id"],
            "tweet_created_at": tweet_created_at,
            "tweet_text": tweet_text,
            "tweet_fk_media_type_id": 1,
            "tweet_image_file_name": image_url,
        }

        response_tweet = {
            "fk_user_id": logged_in_user["id"],
            "tweet_created_at": tweet_created_at,
            "tweet_created_at_formatted": format_time_since_epoch(tweet_created_at),
            "tweet_text": tweet_text,
            "tweet_fk_media_type_id": 1,
            "tweet_image_file_name": image_url,
            "user_name": logged_in_user["name"],
            "user_username": logged_in_user["username"],
            "user_profile_image": logged_in_user["profile_image"],
        }

        ############################################################
        # Connect to the db
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_add_tweet = f"""
            INSERT INTO tweets (fk_user_id, tweet_created_at, tweet_text, tweet_fk_media_type_id, tweet_image_file_name) 
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query_add_tweet, tuple(db_tweet.values()))
        connection.commit()
        response_tweet["tweet_id"] = cursor.lastrowid

        # Success
        response.status = 201
        return response_tweet
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
