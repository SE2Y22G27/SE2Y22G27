'''
    all the import required to read the data dictionary that stores
    the user invoice information and decode the token
'''
import jwt
from source.config import secret
def check_valid_data(data):
    '''
        checks whether the keys are all assigned with a value if not then the user
        have not provided sufficient information to convert the invoice to UBL XML

        Arguments:
            data (dictionary) - all the information required to generate invoice

        Returns:
            bool - if all the required fields are not empty dictionary then the information provided
                   by the user is sufficent to generate an invoice

    '''
    # check if the invoiceTypeCode are correct
    if not check_valid_typecode(data['InvoiceTypeCode']):
        return False

    # check if the allowance are correct
    if not check_valid_allowancecharge(data['AllowanceCharge']):
        return False

    # check if the legalmonetary total are correct
    if not check_valid_legalmonetarytotal(data['LegalMonetaryTotal']):
        return False

    # check if all the invoiceLine are correct
    if not check_valid_invoiceline(data['InvoiceLine']):
        return False

    return True

def check_valid_typecode(data_invoicetypecode):
    '''
        check if the type code field is not empty and
        check if it is a valid invoice type code
    '''
    if data_invoicetypecode == {}:
        return False

    if data_invoicetypecode != 380:
        return False

    return True

def check_valid_allowancecharge(data_allowancecharge):
    '''
        check if all the allowance chage fields are not empty
    '''
    for  value in data_allowancecharge.values():
        if value == {}:
            return False

    for value in data_allowancecharge['TaxCategory'].values():
        if value == {}:
            return False

    if data_allowancecharge['TaxCategory']['ID'] == {}:
        return False

    check_valid_chargeamount(data_allowancecharge['Amount'])

    return True


def check_valid_legalmonetarytotal(data_legalmonetarytotal):
    '''
        check if all the fields in legal monetary total are not empty
    '''
    for value in data_legalmonetarytotal.values():
        if value == {}:
            return False
    check_valid_chargeamount(data_legalmonetarytotal['LineExtensionAmount'])
    check_valid_chargeamount(data_legalmonetarytotal['TaxInclusiveAmount'])
    check_valid_chargeamount(data_legalmonetarytotal['TaxExclusiveAmount'])
    check_valid_chargeamount(data_legalmonetarytotal['ChargedTotalAmount'])
    check_valid_chargeamount(data_legalmonetarytotal['PayableAmount'])

    return True

def check_valid_invoiceline(data_invoiceline):
    '''
        check if all the fields are not empty
    '''
    for  invoice_item in data_invoiceline:
        for value in invoice_item.values():
            if value == {}:
                return False

        if invoice_item['Price']['PriceAmount'] == {}:
            return False

        check_valid_priceamount(invoice_item['Price']['PriceAmount'])

    return True

def check_valid_chargeamount(data_amount):
    '''
        check if charge amount satisfies the condition
    '''
    if data_amount < 0:
        return True

    return False

def check_valid_priceamount(data_amount):
    '''
        check if the price is positive and return bool
    '''
    if data_amount >= 0:
        return True

    return False

def decode_user_invoice(data):
    '''
        return user data dictionary by decoding the jwt token from the
        parameter
    '''
    return jwt.decode(data, secret, algorithms = ['HS256'])
