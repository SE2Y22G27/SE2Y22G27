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
                                'TaxExclusiveAmount' : {},
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

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)

def test_invalid_taxtotal():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

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
                'TaxableAmount' : {},
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

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)



def test_invalid_invoiceline():
    '''
        test if the field hasn't been filled in with data
    '''
    clear()
    register_info = register("test0@gmail.com", "password", "I", "Person")

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
                    'PriceAmount' : {},
                    'BaseQuantity' : 1.0,
                        },
            },
                        ],
                    }

    with pytest.raises(InputError):
        data_read_v1(register_info['token'], sample_dict)
