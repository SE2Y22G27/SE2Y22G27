import json
from source.database import data
from source.helper_auth import check_valid_token

def data_read_v1(token, data):
    '''
    given token (username) and session_id to check whether this user is currently logged into our system
    data is the json_input from the user to be stored under their users dictionary

    Arguments:
        token (string) : Username thats encrypted into JWT token
        data (string) : json data received from the user input

    Exceptions:
        - invalid token
        - data is not valid 

    Returns:
        {}
    
    '''
    database = data.get_data()

    # ----- Error handling -----
    # check whether the token is valid 
    if (not check_valid_token(token)):
        raise Exception("user is not logged in!!!")

    # check if all the required fields have user inputs
    


