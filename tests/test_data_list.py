'''
    import pytest to test if the source code behave what we've expected
'''
from source.data_list import data_list_v1
from source.test_clear import clear
from source.register import register
from source.error import AccessError
from source.data_read import data_read_v1
import pytest

def test_valid_invoice():
    '''
        testing if the invoice is listing porperly
    '''
    clear()
    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")

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
    test_dict = data_list_v1(register_info['token'])

    assert test_dict == sample_dict

def test_empty_invoice():
    '''
        testing when a user haven't enter their input
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

    with pytest.raises(AccessError):
        data_list_v1(register_info['token'])

