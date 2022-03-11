from calendar import c
import pytest
from source.data_read import data_read_v1
from source.database import data
from source.register import register
from source.test_clear import clear
from source.error import InputError

def test_valid_input():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,

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

    data_read_v1(id['token'], sample_dict)         
    test_dict = {}

    data_dict = data.get_data()
    for user in data_dict['users']:
        if user['user_id'] == id['auth_user_id']:
            test_dict = user['user_invoice']
            break

    assert  test_dict == sample_dict

def test_invalid_LegalMonetaryTotal():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,

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
        data_read_v1(id['token'], sample_dict)

def test_invalid_Allowance():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,

                    'AllowanceCharge' :     {
                                                'ChargeIndicator' : 'true',
                                                'AllowanceChargeReason' : {},
                                                'Amount' : -25,
                                                'TaxCatagory' : {   'ID' : 'S',
                                                                    'Percent' : 25.0,
                                                                    'TaxScheme' : { 'ID' : 'VAT'},
                                                                },
                                            }, 

                    'LegalMonetaryTotal' : {    'LineExtensionAmount' : -1300,
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
        data_read_v1(id['token'], sample_dict)

def test_invalid_InvoiceTypeCode():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : {},

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
        data_read_v1(id['token'], sample_dict)

def test_invalid_InvoiceLine():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'InvoiceTypeCode' : 380,

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
                                                        'PriceAmount' : {},
                                                      },
                                        },
                                    ],
                    
                    }

    with pytest.raises(InputError):
        data_read_v1(id['token'], sample_dict)