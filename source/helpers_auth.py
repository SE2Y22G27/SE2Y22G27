'''
This file contains helper functions used in all auth functions.
'''

import uuid
import re
import jwt
import datetime

from source.config import secret
from source.database import data
from source.error import AccessError, InputError

def generate_session_id():
    '''
	Generates a session ID. The session ID is made under the UUID4 rule/system.

	Returns the newly made session ID.
    '''
    session_id = uuid.uuid4()
    return session_id

def generate_token(session_id, user_id):
    '''
	Generates a JSON Web Token (JWT) using the SECRET global variable
	and the HS256 algorithm. The token is created from the session ID and the user ID.
	The token lasts for 30 minutes or 1800 seconds so after that the token will expire.

	Arguments:
		session_id (UUID) - Current session ID
		user_id (integer) - ID of the user

	Returns the token upon creation.
    '''

    info = {
		'session_id': str(session_id),
		'user_id': user_id,
		'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=1800)
	}

    token = jwt.encode(info, secret, algorithm='HS256')
    return token

def decode_token(token):
    '''
	Decodes a JSON Web Token (JWT) using the SECRET global variable
	and the HS256 algorithm.

	Arguments:
		token (string) - Valid JWT

	Returns the User ID of who owns the token
	Returns False if the decoding fails
    '''
    try:
        info = jwt.decode(token, secret, algorithms=['HS256'])
        return info['user_id']
    except:
        return False

def check_valid_token(token):
    '''
	Checks if the token is invalid under 2 checks.
	The first check is to see if the format of the token is correct.
		Format: xxx.yyy.zzz
	The second check is to see if the token is logged in or already expired.

	Arguments:
		token (string) - Token to be checked

	If found invalid, raise an AccessError, if not, nothing is returned.
    '''
    token_format = r'[A-Za-z0-9_%+-]+\.[A-Za-z0-9_%+-]+\.[A-Za-z0-9_%+-]+'
    if not re.fullmatch(token_format, token):
        raise AccessError(description="Invalid token format")
    if re.fullmatch(token_format, token):
        database = data.get_data()
        decoded_u_id = decode_token(token)
        found = False
        if decoded_u_id is False:
            raise AccessError(description="Invalid token")

        for user in database['users']:
            if user['user_id'] == decoded_u_id and found is False:
                found =  True
                user_sessions = user['sessions']
                if token not in user_sessions:
                    raise AccessError(description="Inactive token")

def check_email(email, database):
    '''
	Checks to see if the email format is correct.
	Checks to see if the email already exists in the database.
	If any of these checks fail, raise Exception.

	Arguments:
		email (string) - The inputted email to be checked
		database (Data class) - The data storage
    '''
    email_format = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not re.fullmatch(email_format, email):
        raise InputError(description="Incorrect Email format")

    for user in database['users']:
        if user['email'] == email:
            raise InputError(description="Email already exists")

def check_name_length(first_name, last_name):
    '''
	Checks to see if first and last name is within the set bounds
	1 <= x <= 30.
	If check fails, raise Exception.

	Arguments:
		first_name (string) - First name to be checked
		last_name (string) - Last name to be checked
    '''
    first_length = len(first_name)
    last_length = len(last_name)

    if first_length < 1 or first_length > 30:
        raise InputError(description="First name's length is invalid")
    if last_length < 1 or last_length > 30:
        raise InputError(description="Last name's length is invalid")
