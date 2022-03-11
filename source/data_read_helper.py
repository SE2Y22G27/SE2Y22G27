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
    if not check_valid_InvoiceTypeCode(data['InvoiceTypeCode']):
        return False

    # check if the allowance are correct
    if not check_valid_AllowanceCharge(data['AllowanceCharge']):
        return False

    # check if the legalmonetary total are correct
    if not check_valid_LegalMonetaryTotal(data['LegalMonetaryTotal']):
        return False

    # check if all the invoiceLine are correct
    if not check_valid_InvoiceLine(data['InvoiceLine']):
        return False

    return True

def check_valid_InvoiceTypeCode(data_invoiceTypeCode):

    if data_invoiceTypeCode == {}:
        return False
    
    if data_invoiceTypeCode != 380:
        return False

    return True


def check_valid_AllowanceCharge(data_AllowanceCharge):

    for  value in data_AllowanceCharge.values():
        if value == {}:
            return False

    for value in data_AllowanceCharge['TaxCatagory'].values():
        if value == {}:
            return False
    
    if data_AllowanceCharge['TaxCatagory']['ID'] == {}:
        return False

    check_valid_ChargeAmount(data_AllowanceCharge['Amount'])

    return True

    
        

def check_valid_LegalMonetaryTotal(data_LegalMonetaryTotal):

    for value in data_LegalMonetaryTotal.values():
        if value == {}:
            return False
    check_valid_ChargeAmount(data_LegalMonetaryTotal['LineExtensionAmount'])
    check_valid_ChargeAmount(data_LegalMonetaryTotal['TaxInclusiveAmount'])
    check_valid_ChargeAmount(data_LegalMonetaryTotal['TaxExclusiveAmount'])
    check_valid_ChargeAmount(data_LegalMonetaryTotal['ChargedTotalAmount'])
    check_valid_ChargeAmount(data_LegalMonetaryTotal['PayableAmount'])

    return True

def check_valid_InvoiceLine(data_InvoiceLine):

    for  invoice_item in data_InvoiceLine:
        for value in invoice_item.values():
            if value == {}:
                return False
            
        if invoice_item['Price']['PriceAmount'] == {}:
            return False
        
        check_valid_PriceAmount(invoice_item['Price']['PriceAmount'])

    return True

def check_valid_ChargeAmount(data_amount):
    if data_amount < 0:
        return True

    return False

def check_valid_PriceAmount(data_amount):
    if data_amount >= 0:
        return True

    return False

def decode_user_invoice(data):
		return jwt.decode(data, secret, algorithms = ['HS256'])
'''
def decode_data(data):
    decoded_dictionary = {}
    for key,value in data.items():
        if key == 'AllowanceCharge':
            decoded_dictionary[key] = decode_data(data[key])
        elif key == "TaxCategory":
            decoded_dictionary[key] = decode_data(data[key])
        elif key == 'TaxScheme':
            decoded_dictionary[key] = decode_data(data[key])
        elif key == "LegalMonetarytotal":
            decoded_dictionary[key] = decode_data(data[key])
        elif key == "InvoiceLine":
            decoded_dictionary[key] = decode_data(data[key])
        elif key == "PriceAmount":
            decoded_dictionary[key] = decode_data(data[key])
        else :
            decoded_dictionary['InvoiceTypeCode'] = jwt.decode(data['InvoiceTypeCode'], secret, algorithms=['HS256'])
    return decoded_dictionary
    '''