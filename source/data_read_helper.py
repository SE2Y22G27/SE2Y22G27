from asyncio.windows_events import NULL
from source.database import data

def check_valid_data(data):
    '''
        checks whether the keys are all assigned with a value if not then the user
        have not provided sufficient information to convert the invoice to UBL XML

        Arguments:
            data (dictionary) - all the information required to generate invoice

        Returns:
            bool - if all the required fields are not NULL then the information provided
                   by the user is sufficent to generate an invoice

    '''
    # check if the items are not empty
    for key, value in data.items():
        if value == NULL:
            return False
    
    return check_valid_items(data)

def check_valid_items(data):
    '''
        checks whether the items have correct quantity, amount, and total price amount

        Arguments:
            data (dictionary) - information contains items key

        Returns:
            bool - if all the required fields are not NULL then the items are valid

    '''
    # check if the item is valid but the quantity is NULL
    for quantity in data['items']['invoicedQuantity']:
        if quantity == NULL:
            return False

    # check if the amount is NULL
    for amount in data['items']['lineExtensionAmount']:
        if amount == NULL:
            return False

    # check if the price is NULL
    for price in data['items']['priceAmount']:
        if price == NULL:
            return False

    return True

