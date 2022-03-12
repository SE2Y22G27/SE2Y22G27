from source.data_list import data_list_v1
from source.database import data
from source.test_clear import clear
from source.data_read_helper import decode_user_invoice
from source.register import register
from source.error import AccessError
import pytest
from source.data_read import data_read_v1

def test_valid_invoice():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,

                    'AllowanceCharge' :     {
                                                'ChargeIndicator' : 'true',
                                                'AllowanceChargeReason' : 'Insurance',
                                                'Amount' : -25,
                                                'TaxCategory' : {   'ID' : 'S',
                                                                    'Percent' : 25.0,
                                                                    'TaxScheme' : { 'ID' : 'VAT'},
                                                                },
                                            }, 

                    'LegalMonetaryTotal' : {    'LineExtensionAmount' : -1300,
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

    data_read_v1(id['token'], sample_dict)   
    test_dict = data_list_v1(id['token'])

    assert  test_dict == sample_dict

def test_empty_invoice():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    
    with pytest.raises(AccessError):
        data_list_v1(id['token'])
   