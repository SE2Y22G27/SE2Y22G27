'''
    import pytest test to test all the conditions
'''
import pytest
# from calendar import c
from source.data_read import data_read_v1
from source.database import data
from source.register import register
from source.test_clear import clear
from source.error import InputError
from source.data_read_helper import decode_user_invoice


def test_valid_input():
    '''
        test for valid input if the function is behaving normally
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,
        'AllowanceCharge' : {
            'ChargeIndicator' : 'true',
            'AllowanceChargeReason' : 'Insurance',
            'Amount' : -25,
            'TaxCategory' : {   'ID' : 'S',
                'Percent' : 25.0,
                'TaxScheme' : { 'ID' : 'VAT'},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : -1300,
                                'TaxExclusiveAmount' : -1000,
                                'TaxInclusiveAmount' : -1656.25,
                                'ChargedTotalAmount' : -25,
                                'PayableAmount' : -1656.25,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : -7,
                'LineExtensionAmount' : -2800,
                'Price' : {
                    'PriceAmount' : 400,
                        },
            },
            {
                'ID' : 2,
                'InvoiceQuantity' : 3,
                'LineExtensionAmount' : 1500,
                'Price' : {
                    'PriceAmount' : 500,
                            },
            },
                        ],
                    }

    data_read_v1(register_info['token'], sample_dict)
    test_dict = {}

    data_dict = data.get_data()
    for user in data_dict['users']:
        if user['user_id'] == register_info['auth_user_id']:

            test_dict = user['user_invoice']
            break
    test_dict = decode_user_invoice(test_dict)

    assert test_dict == sample_dict

def test_invalid_legalmonetarytotal():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,
        'AllowanceCharge' : {
            'ChargeIndicator' : 'true',
            'AllowanceChargeReason' : 'Insurance',
            'Amount' : -25,
            'TaxCategory' : {   'ID' : 'S',
                'Percent' : 25.0,
                'TaxScheme' : { 'ID' : 'VAT'},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : -1300,
                                'TaxExclusiveAmount' : {},
                                'TaxInclusiveAmount' : -1656.25,
                                'ChargedTotalAmount' : -25,
                                'PayableAmount' : -1656.25,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : -7,
                'LineExtensionAmount' : -2800,
                'Price' : {
                    'PriceAmount' : 400,
                        },
            },
            {
                'ID' : 2,
                'InvoiceQuantity' : 3,
                'LineExtensionAmount' : 1500,
                'Price' : {
                    'PriceAmount' : 500,
                            },
            },
                        ],
                    }

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)

def test_invalid_allowance():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,
        'AllowanceCharge' : {
            'ChargeIndicator' : 'true',
            'AllowanceChargeReason' : {},
            'Amount' : -25,
            'TaxCategory' : {   'ID' : 'S',
                'Percent' : 25.0,
                'TaxScheme' : { 'ID' : 'VAT'},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : -1300,
                                'TaxExclusiveAmount' : -1000,
                                'TaxInclusiveAmount' : -1656.25,
                                'ChargedTotalAmount' : -25,
                                'PayableAmount' : -1656.25,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : -7,
                'LineExtensionAmount' : -2800,
                'Price' : {
                    'PriceAmount' : 400,
                        },
            },
            {
                'ID' : 2,
                'InvoiceQuantity' : 3,
                'LineExtensionAmount' : 1500,
                'Price' : {
                    'PriceAmount' : 500,
                            },
            },
                        ],
                    }

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)

def test_invalid_invoicetypecode():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")


    sample_dict = { 'InvoiceTypeCode' : {},
        'AllowanceCharge' : {
            'ChargeIndicator' : 'true',
            'AllowanceChargeReason' : 'Insurance',
            'Amount' : -25,
            'TaxCategory' : {   'ID' : 'S',
                'Percent' : 25.0,
                'TaxScheme' : { 'ID' : 'VAT'},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : -1300,
                                'TaxExclusiveAmount' : -1000,
                                'TaxInclusiveAmount' : -1656.25,
                                'ChargedTotalAmount' : -25,
                                'PayableAmount' : -1656.25,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : -7,
                'LineExtensionAmount' : -2800,
                'Price' : {
                    'PriceAmount' : 400,
                        },
            },
            {
                'ID' : 2,
                'InvoiceQuantity' : 3,
                'LineExtensionAmount' : 1500,
                'Price' : {
                    'PriceAmount' : 500,
                            },
            },
                        ],
                    }

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)

def test_invalid_invoiceline():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,
        'AllowanceCharge' : {
            'ChargeIndicator' : 'true',
            'AllowanceChargeReason' : 'Insurance',
            'Amount' : -25,
            'TaxCategory' : {   'ID' : 'S',
                'Percent' : 25.0,
                'TaxScheme' : { 'ID' : 'VAT'},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : {},
                                'TaxExclusiveAmount' : -1000,
                                'TaxInclusiveAmount' : -1656.25,
                                'ChargedTotalAmount' : -25,
                                'PayableAmount' : -1656.25,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : -7,
                'LineExtensionAmount' : -2800,
                'Price' : {
                    'PriceAmount' : 400,
                        },
            },
            {
                'ID' : 2,
                'InvoiceQuantity' : 3,
                'LineExtensionAmount' : 1500,
                'Price' : {
                    'PriceAmount' : 500,
                            },
            },
                        ],
                    }

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)

