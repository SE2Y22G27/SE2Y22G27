def check_valid_data(data):
    '''
        checks whether the keys are all assigned with a value if not then the user
        have not provided sufficient information to convert the invoice to UBL XML

        Arguments:
            data (dictionary) - all the information required to generate invoice

        Returns:
            bool - if all the required fields are not empty dictionary then the information provided
                   by the user is sufficent to generate an invoice

    '''
    # check if the items are not empty
    for key, value in data.items():
        if value == {}:
            return False
    
    return check_valid_items(data['items'])

def check_valid_items(data_items):
    '''
        checks whether the items have correct quantity, amount, and total price amount

        Arguments:
            data (dictionary) - information contains items key

        Returns:
            bool - if all the required fields are not empty dictionary then the items are valid

    '''
    # check if the item is valid by checking if all the keys are not {}
    for item in data_items:
        for key,value in item.items():
            if value == {}:
                return False

    return True

