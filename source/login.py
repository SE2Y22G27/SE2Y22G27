import hashlib

from source.error import InputError
from source.database import data
from source.helpers_auth import generate_session_id, generate_token

def login(email: str, password: str):
    '''
	Given an email and password, logs the user into the service.

	Arguments:
		email (string) - Email of the user
		password (string) - Password of the user

	Exceptions:
		(*) All exceptions are InputErrors
		- Email does not exist in the database
		- Password is incorrect

	Returns:
		The authorized user id and token of the user.
    '''
    database = data.get_data()
    u_id = 0
    current_token = 0
    email_exist = False
    correct_password = False

	# Check if the email exists firsts,
	# if email exists then check password next
	# This should create a session ID and token
	# for the user to login.
    for user in database['users']:
        if user['email'] == email:
            email_exist = True
            check_password = hashlib.sha256(password.encode()).hexdigest()
            if check_password == user['password']:
                correct_password = True
                temp_session = generate_session_id()
                u_id = user['user_id']
                current_token = generate_token(temp_session, u_id)
                user['sessions'][current_token] = temp_session

	# ----- Error handling -----
    if email_exist is False:
        raise InputError(description="This email does not exist")
    if correct_password is False:
        raise InputError(description="Incorrect password")
	# ----- End of Error handling -----

    data.save_data(database)
    return {
        'auth_user_id': u_id,
        'token': current_token,
    }
