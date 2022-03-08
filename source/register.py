from source.database import data
from source.helpers_auth import generate_session_id, generate_token, decode_token, check_valid_token, check_email, check_name_length
import hashlib

def register(email: str, password: str, first_name: str, last_name: str):
	'''
	Given an email, password, first and last name, register an account for the user
	and save the user info in the database

	Arguments:
		email (string) - Email of the user
		password (string) - Password of the user
		first_name (string) - First name of the user
		last_name (string) - Last name of the user

	Exceptions:
		- Incorrect email format
		- If inputted email already exists
		- First name length < 1 or > 30
		- Last name length < 1 or > 30
		- Password length < 8

	Returns:
		The authorized user id and token of the newly-registered user.
	'''
	database = data.get_data()

	# ----- Error handling -----
	# Check correct email format and if it exists in the database
	check_email(email, database)

	# Check if the names is of sufficient length
	check_name_length(first_name, last_name)

	# Check if the password is of sufficient length
	if len(password) < 8:
		raise Exception("Password is too short")

	# ----- End of Error handling -----

	id = len(database['users'])
	hashed_password = hashlib.sha256(password.encode()).hexdigest()

	temp_session = generate_session_id()
	token = generate_token(temp_session, id)

	user_info = {
		'user_id': id,
		'email': email,
		'password': hashed_password,
		'first_name': first_name,
		'last_name': last_name,
		'sessions': {token: temp_session},
	}
	database['users'].append(user_info)
	data.save_data(database)
	return {
		'auth_user_id': id,
		'token': token,
	}