import pytest
from source.create_xml import create_invoice_v1
from source.database import data
from source.test_clear import clear

@pytest.fixture
def initial_clear():
    clear()

@pytest.fixture
def invoice_data():
    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
    
    sample_data = {
        'InvoiceTypeCode':380,

        'AllowanceCharge': {
            'ChargeIndicator':1,
            'AllowanceChargeReason':1,
            'Amount':1,
            'TaxCategory': {
                'ID':1,
                'Percent':1,
                'TaxScheme': {
                    'ID':1,
                },
            },
        },

        'LegalMonetaryTotal': {
            'LineExtensionAmount':1,
            'TaxExclusiveAmount':1,
            'TaxInclusiveAmount':1,
            'ChargedTotalAmount':1,
            'PayableAmount':1,
        },

        'InvoiceLine': [
            {
                'ID':1,
                'InvoicedQuantity':1,
                'LineExtensionAmount':1,
                'Price': {
                    'PriceAmount':1,
                },
            }
        ],
    }

    data_read_v1(register_info['token'], sample_data)

    return register_info



def test_valid_input(initial_clear, invoice_data):
    # Takes the token of the user, will search database for user
    # Then takes first invoice made which will contain all the details
    
    # When this test is run check if a file has been created with the above information
    assert create_invoice_v1(invoice_data['token']) == {}