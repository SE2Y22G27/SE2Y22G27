import json
from source.database import data as database
from source.helpers_auth import check_valid_token, decode_token
from source.data_read_helper import check_valid_data
from source.error import InputError, AccessError

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
    data_info = database.get_data()

    # ----- Error handling -----
    # check whether the token is valid 
    check_valid_token(token)

    # check if all the required fields have user inputs
    if not check_valid_data(data):
        raise InputError("no sufficient information to create an invoice")

    user_id = decode_token(token)

    invoice_dict =  {
                    'InvoiceTypeCode' : data['InvoiceTypeCode'],

                    'AllowanceCharge' :     {
                                                'ChargeIndicator' : data['AllowanceCharge']['ChargeIndicator'],
                                                'AllowanceChargeReason' : data['AllowanceCharge']['AllowanceChargeReason'],
                                                'Amount' : data['AllowanceCharge']['Amount'],
                                                'TaxCatagory' : {   'ID' : data['AllowanceCharge']['TaxCatagory']['ID'],
                                                                    'Percent' : data['AllowanceCharge']['TaxCatagory']['Percent'],
                                                                    'TaxScheme' : { 'ID' : data['AllowanceCharge']['TaxCatagory']['TaxScheme']['ID']},
                                                                },
                                            }, 

                    'LegalMonetaryTotal' : {    'LineExtensionAmount' : data['LegalMonetaryTotal']['LineExtensionAmount'],
                                                'TaxExclusiveAmount' : data['LegalMonetaryTotal']['TaxExclusiveAmount'],
                                                'TaxInclusiveAmount' : data['LegalMonetaryTotal']['TaxInclusiveAmount'],
                                                'ChargedTotalAmount' : data['LegalMonetaryTotal']['ChargedTotalAmount'],
                                                'PayableAmount' : data['LegalMonetaryTotal']['PayableAmount'],
                                            },

                    'InvoiceLine' : [],
                    }

    invoiceLine = {}

    for items in data['InvoiceLine']:
        invoice_dict['InvoiceLine'].append(items)

    for user in data_info['users']:
        if user["user_id"] == user_id:
            user['user_invoice'] = invoice_dict
            break

    database.save_data(data_info)
