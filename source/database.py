'''
This file contains a definition of a class called Database which our program will use to
store data. It will be usable with data persistence later on once we've used
the pickle python module.

Usage:

    from database import data

    database = data.get_data()	# Gets the data from the database
    print(database) # Prints { 'users': [{'user_id': 1, 'name': 'Raymond'},
    {'user_id': 2, 'name': 'Zeu'}] }

    users = database['users']

    users.pop(0) 	# Removes the item in index 0 of the list, this case, the item with user_id 1
    users.append({'user_id': 3, 'name': 'Yuqiang'})

    data.save_data(database)	# Saves the data to the database
'''
import pickle


data_object = {
    'users': [],
}

class Database:
    '''
        class that contains all the function that read and store
        the user informations as dictionary
    '''
    def __init__(self):
        self.__data = data_object
        try:
            with open('data_storage.p', 'rb') as file:
                self.__data = pickle.load(file)
        except FileNotFoundError:
            print("There is no data to persist at the moment")

    def get_data(self):
        '''
            returns the current data dictionary stored inside data
        '''
        return self.__data

    def save_data(self, new):
        '''
            save the new updated data dictionary into current data
        '''
        if not isinstance(new, dict):
            raise TypeError("not type dictionary")
        self.__data = new

        with open('data_storage.p', 'wb') as file:
            pickle.dump(self.__data, file)


print("Loading Database...")

data = Database()
