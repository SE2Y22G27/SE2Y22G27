#import pytest
from register import register
from data_read import data_read_v1
from create_xml import create_invoice_v1
from database import data
from test_clear import clear


if __name__ == '__main__':
    initial_clear()
    register_info = invoice_data()
    test_valid_input(register_info)


#@pytest.fixture
def initial_clear():
    clear()

#@pytest.fixture
def invoice_data():
    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
    
    sample_data = { 'InvoiceTypeCode' : 380,

                    'AllowanceCharge' :     {
                                                'ChargeIndicator' : 'true',
                                                'AllowanceChargeReason' : 'Insurance',
                                                'Amount' : -25,
                                                'TaxCatagory' : {   'ID' : 'S',
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

    data_read_v1(register_info['token'], sample_data)

    return register_info



def test_valid_input(invoice_data):
    # Takes the token of the user, will search database for user
    # Then takes first invoice made which will contain all the details
    
    # When this test is run check if a file has been created with the above information
    assert create_invoice_v1(invoice_data['token']) == {}