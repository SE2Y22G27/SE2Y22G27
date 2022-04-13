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
