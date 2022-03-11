import json
import jwt
from source.config import secret
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
    '''
    invoice_dict =  {
                    'InvoiceTypeCode' : jwt.encode(data['InvoiceTypeCode'], secret, algorithms = 'HS256'),

                    'AllowanceCharge' :     {
                                                'ChargeIndicator' : jwt.encode(data['AllowanceCharge']['ChargeIndicator'], secret, algorithms='HS256'),
                                                'AllowanceChargeReason' : jwt.encode(data['AllowanceCharge']['AllowanceChargeReason'], secret, algorithms='HS256'),
                                                'Amount' : jwt.encode(data['AllowanceCharge']['Amount'], secret, algorithms='HS256'),
                                                'TaxCatagory' : {   'ID' : jwt.encode(data['AllowanceCharge']['TaxCatagory']['ID'], secret, algorithms='HS256'),
                                                                    'Percent' : jwt.encode(data['AllowanceCharge']['TaxCatagory']['Percent'], secret, algorithms='HS256'),
                                                                    'TaxScheme' : { 'ID' : jwt.encode(data['AllowanceCharge']['TaxCatagory']['TaxScheme']['ID'], secret, algorithms='HS256')},
                                                                },
                                            }, 

                    'LegalMonetaryTotal' : {    'LineExtensionAmount' : jwt.encode(data['LegalMonetaryTotal']['LineExtensionAmount'], secret, algorithms='HS256'),
                                                'TaxExclusiveAmount' : jwt.encode(data['LegalMonetaryTotal']['TaxExclusiveAmount'], secret, algorithms='HS256'),
                                                'TaxInclusiveAmount' : jwt.encode(data['LegalMonetaryTotal']['TaxInclusiveAmount'], secret, algorithms='HS256'),
                                                'ChargedTotalAmount' : jwt.encode(data['LegalMonetaryTotal']['ChargedTotalAmount'], secret, algorithms='HS256'),
                                                'PayableAmount' : jwt.encode(data['LegalMonetaryTotal']['PayableAmount'], secret, algorithms='HS256'),
                                            },

                    'InvoiceLine' : [],
                    }
    '''
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
    '''
    for items in data['InvoiceLine']:
        invoice_dict['ID'] = jwt.encode(items['ID'], secret, algorithms='HS256')
        invoice_dict['InvoiceQuantity'] = jwt.encode(items['InvoicedQuantity'], secret, algorithms='HS256')
        invoice_dict['LineExtensionAmount'] = jwt.encode(items['LineExtensionAmount'], secret, algorithms='HS256')
        invoice_dict['price']['PriceAmount'] = jwt.encode(items['Price']['PriceAmount'], secret, algorithms='HS256')
    '''

    for items in data['InvoiceLine']:
        invoice_dict['InvoiceLine'].append(items)

    for user in data_info['users']:
        if user["user_id"] == user_id:
            user['user_invoice'] = jwt.encode(invoice_dict, secret, algorithm= 'HS256')
            break

    database.save_data(data_info)
