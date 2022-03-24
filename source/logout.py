from source.helpers_auth import check_valid_token, decode_token
from source.database import data

def logout(token):
    '''
	Given an active token, logs the user out of the service and
	ends their current session.

	Arguments:
		token (string) - Active token of a session of the user

	Exceptions:
		(*) All errors are AccessErrors
		- If the token is invalid/inactive

	Returns:
		Nothing is returned, the user is logged out of their session.
    '''
	# Error is if token is invalid
    check_valid_token(token)

	# If we reach here, then that means the token is valid.
    database = data.get_data()
    found = False
    decoded_u_id = decode_token(token)

    for user in database['users']:
        if decoded_u_id == user['user_id'] and found is False:
            found = True
            user['sessions'].pop(token)

    data.save_data(database)
