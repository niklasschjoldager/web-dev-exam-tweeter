from bottle import delete, response
from mysql import connector

from g import DATABASE_CONFIG
from utils import get_logged_in_user, validate_user_session

############################################################
@delete("/users/<user_to_id:int>/unfollow")
def _(user_to_id):
    connection, cursor = None, None

    try:
        validate_user_session()
        logged_in_user = get_logged_in_user()

        if user_to_id < 1:
            response.status = 400
            return {"info": "User ID is not a valid ID"}

        # Connect to the db
        connection = connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_unfollow_user = f"""
            DELETE FROM followers
            WHERE fk_user_from_id = %(fk_user_from_id)s AND fk_user_to_id = %(fk_user_to_id)s
        """

        unfollow_user = {
            "fk_user_from_id": logged_in_user["id"],
            "fk_user_to_id": user_to_id,
        }

        cursor.execute(query_unfollow_user, unfollow_user)
        connection.commit()

        response.status = 200
        return {"info": "Unfollowed user with ID"}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Oops, something went wrong"}
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()
