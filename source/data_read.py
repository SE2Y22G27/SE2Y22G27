import json
from source.database import data as database
from source.helpers_auth import check_valid_token, decode_token
from source.data_read_helper import check_valid_data

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
    if not check_valid_token(token):
        raise Exception("user is not logged in!!!")

    # check if all the required fields have user inputs
    if not check_valid_data(data):
        raise Exception("not sufficient information to create an invoice")

    user_id = decode_token(token)

    invoice_dict =  {'Amount' : data['Amount'], 
                    'lineExtensionAmount' : data['lineExtensionAmount'],
                    'taxExclusiveAmount' : data['taxExclusiveAmount'],
                    'taxInclusiveAmount' : data['taxInclusiveAmount'],
                    'chargeTotalAmount' : data['chargedTotalAmount'],
                    'payableAmount' : data['payableAmount'],
                    'items' : [],
                    }

    for items in data['items']:
        invoice_dict['items'].append(items)

    for user in database['users']:
        if user["user_id"] == user_id:
            user['user_invoices'].append(invoice_dict)
            break


