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

    sample_dict = { 'invoiceID' : 1,
                    'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : 9,
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{'invoiceQuantity' : 5, 'lineExtensionAmount' : 15, 'priceAmount' : 26.61},],
                    }

    data_read_v1(id['token'], sample_dict)         
    user_invoices = {}
    test_dict = {}
    data.load_data()
    data_dict = data.get_data()
    for user in data_dict['users']:
        if user['user_id'] == id['auth_user_id']:
            user_invoices = user['user_invoices']
            break

    for invoice in user_invoices:
        if invoice['invoiceID'] == 1:
            test_dict = invoice
            break

    assert  test_dict == sample_dict

def test_invalid_taxInclusiveAmount():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : {},
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{'invoiceQuantity' : 5, 'lineExtensionAmount' : 15, 'priceAmount' : 26.61},],
                    }
    with pytest.raises(InputError):
        data_read_v1(id['token'], sample_dict)

def test_invalid_taxInclusiveAmount():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : {},
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{'invoiceQuantity' : 5, 'lineExtensionAmount' : 15, 'priceAmount' : 26.61},],
                    }

    with pytest.raises(InputError):
        data_read_v1(id['token'], sample_dict)

def test_invalid_items():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : {},
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{}],
                    }

    with pytest.raises(InputError):
        data_read_v1(id['token'], sample_dict)

def test_invalid_item_information():
    clear()
    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : {},
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{'invoiceQuantity' : {}, 'lineExtensionAmount' : 15, 'priceAmount' : 26.61},],
                    }

    with pytest.raises(InputError):
        data_read_v1(id['token'], sample_dict)