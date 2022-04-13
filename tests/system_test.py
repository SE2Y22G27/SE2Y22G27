import pytest
from source.register import register
from source.login import login
from source.logout import logout
from source.data_read import data_read_v1
from source.data_list import data_list_v1
from source.test_clear import clear


@pytest.fixture
def initial_clear():
    '''
    Clearing the database
    '''
    clear()

def test_system(initial_clear): # initial_clear
    '''
    Test if register is successful
    When registering you automatically login
    '''
    initial_clear
    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
    assert register_info['auth_user_id'] == 0

    # No error should be called for successful logout
    logout(register_info['token'])

    # Test if login is successful
    login_id = login("testA@gmail.com", "1234567890")
    assert register_info['auth_user_id'] == login_id['auth_user_id']
    assert register_info['token'] != login_id['token']

    # Test if data is properly read and returned in the correct format
    sample_dict = { 
        'InvoiceTypeCode' : 380,
        'IssueDate' : '2022-02-07',
        'AccountingSupplierParty' : {
            'Party' : 
                    {
                        'PartyIdentification': {'ID': 80647710156},
                        'PartyName' : {'Name': 'Ebusiness Software Services Pty Ltd'},
                        'PostalAddress' : {
                                'StreetName' : '100 Business St',
                                'CityName': 'Dulwich Hill',
                                'PostalZone' : 2203,
                                'Country' : {'IdentificationCode': 'AU'}
                        },
                        'PartyLegalEntity' : {
                            'RegistrationName' : 'Ebusiness Software Services Pty Ltd',
                            'CompanyID' : 80647710156,
                        }
                    }

                                     },
        'AccountingCustomerParty' : {
            'Party' : 
                    {
                        'PartyName' : {'Name': 'Awolako Enterprises Pty Ltd'},
                        'PostalAddress' : {
                                'StreetName' : 'Suite 123 Level 45',
                                'AdditionalStreetName' : '999 The Crescent',
                                'CityName': 'Homebush West',
                                'PostalZone' : 2140,
                                'Country' : {'IdentificationCode': 'AU'}
                        },
                        'PartyLegalEntity' : {
                            'RegistrationName' : 'Awolako Enterprises Pty Ltd',
                        }
                    }

                                     },
        'PaymentMeans': {
            'PaymentMeansCode' : 1,
            'PaymentID' : 'EBWASP1002',
                        },
        'PaymentTerms': {
            'Note' : 'As agreed'
                        },

        'TaxTotal' : {
            'TaxAmount' : 10.00,
            'TaxSubtotal' : {
                'TaxableAmount' : 100.00,
                'TaxAmount' : 10.00,
                'TaxCategory' : {  
                     'ID' : 'S',
                'Percent' : 10.0,
                'TaxScheme' : { 
                    'ID' : 'GST'
                             }
                                },
                    },

                    },
            

        'LegalMonetaryTotal' : {'LineExtensionAmount' : 100.00,
                                'TaxExclusiveAmount' : 100.00,
                                'TaxInclusiveAmount' : 110.00,
                                'PayableRoundingAmount' : 0.00,
                                'PayableAmount' : 110.00,
                                },

        'InvoiceLine' : [
            {
                'ID' : 1,
                'InvoiceQuantity' : 500.0,
                'LineExtensionAmount' : 100.00,
                'Item' : {
                    'Name' : 'pencils',
                    'ClassifiedTaxCategory': {
                        'ID':'S',
                        'Percent': 10.0,
                        'TaxScheme': {'ID' : 'GST'},
                    },
                },
                'Price' : {
                    'PriceAmount' : 0.20,
                    'BaseQuantity' : 1.0,
                        },
            },
                        ],
                    }

    data_read_v1(login_id['token'], sample_dict)
    test_dict = data_list_v1(login_id['token'])

    assert test_dict == sample_dict

    # Need to check if an xml file is created in the proper format.
    # assert create_invoice_v1(invoice_data['token']) == {}
