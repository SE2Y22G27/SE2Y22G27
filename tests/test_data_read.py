import pytest
from source.data_read import data_read_v1
from source.register import register
from source.test_clear import clear

def test_valid_input():

    id = register("test0@gmail.com", "password", "I", "Person")

    sample_dict = { 'Amount' : 10, 
                    'lineExtensionAmount' : 6,
                    'taxExclusiveAmount' : 4,
                    'taxInclusiveAmount' : 9,
                    'chargeTotalAmount' : 332.6,
                    'payableAmount' : 332.6,
                    'items' : [{'invoiceQuantity' : 5, 'lineExtensionAmount' : 15, 'priceAmount' : 26.61},],
                    }

    with pytest.raises(Exception):
        data_read_v1(id['token'], sample_dict)
