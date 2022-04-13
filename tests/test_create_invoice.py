'''
    import pytest to test all the test cases
'''
from source.register import register
from source.data_read import data_read_v1
from source.create_xml import create_invoice_v1
from source.test_clear import clear



def test_valid_input():
    ''' test if the create_invoice_v1 are working'''
    # Takes the token of the user, will search database for user
    # Then takes first invoice made which will contain all the details
    # When this test is run check if a file has been created with the above information
    clear()

    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")

    sample_data = {
        'InvoiceID' :'EBWASP1002',
        'InvoiceTypeCode' : 380,
        'IssueDate' : '2022-02-07',
        'AccountingSupplierParty' : {
            'Party' :
                    {
                        'PartyIdentification': {'ID': 80647710156},
                        'PartyName' : {'Name': 'Ebusiness Software Services Pty Ltd'},
                        'PostalAddress' : {
                                'StreetName' : '100 Business St',
                                'AdditionalStreetName' : {},
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
                'InvoicedQuantity' : 500.0,
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

    data_read_v1(register_info['token'], sample_data)

    assert not create_invoice_v1(register_info['token'])
