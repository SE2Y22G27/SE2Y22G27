'''
    all the import required to read the data dictionary that stores
    the user invoice information and decode the token
'''
import jwt
from source.config import secret
from datetime import datetime
import time
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
    for info in data.values():
        if info == {}:
            return False

    # check if the invoiceTypeCode are correct
    if not check_valid_typecode(data['InvoiceTypeCode']):
        return False

    # check if the allowance are correct
    if not check_valid_taxtotal(data['TaxTotal']):
        return False

    # check if the legalmonetary total are correct
    if not check_valid_legalmonetarytotal(data['LegalMonetaryTotal']):
        return False

    # check if all the invoiceLine are correct
    if not check_valid_invoiceline(data['InvoiceLine']):
        return False

    if not check_valid_issuedate(data['IssueDate']):
        return False

    if not check_valid_supplier(data['AccountingSupplierParty']['Party']):
        return False

    if not check_valid_customer(data['AccountingCustomerParty']['Party']):
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

def check_valid_issuedate(data_issuedate):
    '''
        check if the issue date is valid
    '''
    if data_issuedate == {}:
        return False

    if data_issuedate > datetime.now().strftime("%Y-%m-%d"):
        return False

    return True

def check_valid_paymentmean(data_paymentmean):
    '''
        check if the payment mean is valid
    '''
    if data_paymentmean == {}:
        return False

    for info in data_paymentmean:
        if info.values() == {}:
            return False
    return True

def check_valid_payment_term(data_payment_term):
    '''
        check if the payment terms is valid
    '''
    if data_payment_term == {}:
        return False

    if data_payment_term['Note'] == {}:
        return False
    
    return True


def check_valid_taxtotal(data_taxtotal):
    '''
        check if all the allowance chage fields are not empty
    '''
    for  value in data_taxtotal.values():
        if value == {}:
            return False

    for value in data_taxtotal['TaxSubtotal'].values():
        if value == {}:
            return False

    for value in data_taxtotal['TaxSubtotal']['TaxCategory'].values():
        if value == {}:
            return False

    if  data_taxtotal['TaxSubtotal']['TaxCategory']['TaxScheme']['ID'] == {}:
            return False

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
    check_valid_chargeamount(data_legalmonetarytotal['PayableRoundingAmount'])
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

        for value in invoice_item['Item'].values():

            if value == {}:
                return False

        for value in invoice_item['Item']['ClassifiedTaxCategory'].values():

            if value == {}:
                return False

        if  invoice_item['Item']['ClassifiedTaxCategory']['TaxScheme']['ID'] == {}:
            return False

        if invoice_item['Price']['PriceAmount'] == {}:
            return False
            
        if invoice_item['Price']['BaseQuantity'] == {}:
            return False

        check_valid_priceamount(invoice_item['Price']['PriceAmount'])
        check_valid_priceamount(invoice_item['Price']['BaseQuantity'])

    return True

def check_valid_supplier(data_supplier):
    '''
        check if all the fields are not empty
    '''
    for info in data_supplier:
        if info == {}:
            return False

    
    if  data_supplier['PartyIdentification']['ID'] == {}:
            return False

    if  data_supplier['PartyName']['Name'] == {}:
            return False
    for supplier_info in data_supplier['PostalAddress']:
            if  supplier_info == {}:
                return False
    if data_supplier['PostalAddress']['Country']['IdentificationCode'] == {}:
            return False
    if  data_supplier['PartyLegalEntity']['RegistrationName'] == {}:
            return False
    if  data_supplier['PartyLegalEntity']['CompanyID'] == {}:
            return False

    return True

def check_valid_customer(data_customer):
    '''
        check if all the fields are not empty
    '''
    for info in data_customer:
        if info == {}:
            return False


    if  data_customer['PartyName']['Name'] == {}:
            return False
    for supplier_info in data_customer['PostalAddress']:
            if  supplier_info == {}:
                return False
    if data_customer['PostalAddress']['Country']['IdentificationCode'] == {}:
            return False
    if  data_customer['PartyLegalEntity']['RegistrationName'] == {}:
            return False

    return True

def check_valid_chargeamount(data_amount):
    '''
        check if charge amount satisfies the condition
    '''
    if int(data_amount) >= 0:
        return True

    return False

def check_valid_priceamount(data_amount):
    '''
        check if the price is positive and return bool
    '''
    if int(data_amount) >= 0:
        return True

    return False

def decode_user_invoice(data):
    '''
        return user data dictionary by decoding the jwt token from the
        parameter
    '''
    return jwt.decode(data, secret, algorithms = ['HS256'])
