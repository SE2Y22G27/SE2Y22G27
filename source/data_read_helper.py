from asyncio.windows_events import NULL
from source.database.py import data

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


    for key, value in data.items():
        if value == NULL:
            return False
    return True