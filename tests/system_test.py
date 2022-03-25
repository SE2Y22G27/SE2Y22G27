import pytest
from source.register import register
from source.login import login
from source.logout import logout
from source.data_read import data_read_v1
from source.data_list import data_list_v1
from source.create_xml import create_invoice_v1
from source.test_clear import clear


@pytest.fixture
def reset():
    """ Function for clearing the data before the test """
    clear()

def test_system(reset):
    '''
    Test if register is successful
    When registering you automatically login
    '''

    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
    assert register_info['auth_user_id'] == 0

    # No error should be called for successful logout
    logout(register_info['token'])

    # Test if login is successful
    login_id = login("testA@gmail.com", "1234567890")
    assert register_info['auth_user_id'] == login_id['auth_user_id']
    assert register_info['token'] != login_id['token']

    # Test if data is properly read and returned in the correct format
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

    data_read_v1(login_id['token'], sample_dict)
    test_dict = data_list_v1(login_id['token'])

    assert test_dict == sample_dict

    # Need to check if an xml file is created in the proper format.
    assert not create_invoice_v1(login_id['token'])
    reset
