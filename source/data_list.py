from source.database import data
from source.helpers_auth import check_valid_token, decode_token
from source.data_read_helper import decode_user_invoices
import json

def data_list_v1(token):
    check_valid_token(token)

    user_id = decode_token(token)

    for user in data['users']:
        if user['user_id'] == user_id:
            invoice_dict = decode_user_invoices(user['user_invoice'])
            json.dumps(invoice_dict)
            break