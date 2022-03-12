from source.database import data
from source.helpers_auth import check_valid_token, decode_token
from source.data_read_helper import decode_user_invoice
from source.error import AccessError
import json

def data_list_v1(token):
    '''
        Gets the user token and print their saved invoice information

        Arguments:
            token(String) : jwt token that stores user id

        Returns:
            return the dictionary of invoice information
    '''

    check_valid_token(token)

    user_id = decode_token(token)

    data_dict = data.get_data()

    for user in data_dict['users']:
        if user['user_id'] == user_id:
            if user['user_invoice'] == {}:
                raise AccessError("you have saved any invoice in your account")
            else:
                invoice_dict = decode_user_invoice(user['user_invoice'])
                return invoice_dict
            break
