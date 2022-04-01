from bottle import put, response

############################################################
@put("/users/<user_id:int>/follow")
def _(user_id):

    try:
        if user_id < 1:
            response.status = 400
            return {"info": "User ID is not a valid ID"}

        response.status = 200
        return {"info": "Followed"}
    except Exception as ex:
        response.status = 500
        return {"info": "Oops, something went wrong"}
