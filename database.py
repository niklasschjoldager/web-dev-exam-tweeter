def get_who_to_follow(logged_in_user_id, cursor):
    query = f"""
        SELECT
            users.user_id,
            users.user_name,
            users.user_username,
            users.user_profile_image,
            COUNT(is_followed_by_logged_in_user.fk_user_to_id) AS is_followed_by_logged_in_user
        FROM users
            
        LEFT JOIN followers AS is_followed_by_logged_in_user
            ON is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id

        WHERE NOT users.user_id = %(logged_in_user_id)s

        GROUP BY users.user_id
        HAVING COUNT(is_followed_by_logged_in_user.fk_user_from_id = %(logged_in_user_id)s AND is_followed_by_logged_in_user.fk_user_to_id = users.user_id) < 1
        LIMIT 3
    """
    params = {"logged_in_user_id": logged_in_user_id}

    cursor.execute(query, params)
    who_to_follow = cursor.fetchall()
    return who_to_follow
