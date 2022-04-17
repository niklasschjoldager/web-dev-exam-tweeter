DATABASE_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "127.0.0.1",
    "port": 8889,
    "database": "tweeter_exam",
}
JSON_WEB_TOKEN_SECRET = "699js!ihTri94t@sa129d90waj0cjh428h824h5298h"

###########################################################
TWEET_TEXT_MIN_LENGTH = 1
TWEET_TEXT_MAX_LENGTH = 255
TWEET_IMAGE_PATH = "../client/static/tweets"

IMAGE_ALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]

USER_BIO_MAX_LENGTH = 160
USER_BIO_MIN_LENGTH = 1
USER_LOCATION_MAX_LENGTH = 30
USER_LOCATION_MIN_LENGTH = 1
USER_NAME_MAX_LENGTH = 50
USER_NAME_MIN_LENGTH = 2
USER_USERNAME_MAX_LENGTH = 20
USER_USERNAME_MIN_LENGTH = 4
USER_PASSWORD_MIN_LENGTH = 8
USER_WEBSITE_MAX_LENGTH = 100
USER_WEBSITE_MIN_LENGTH = 1
USER_IMAGE_PATH = "../client/static/users"

###########################################################
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"
