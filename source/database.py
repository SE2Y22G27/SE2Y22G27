import json
import pickle

'''
This file contains a definition of a class called Database which our program will use to
store data. It will be usable with data persistence later on once we've used
the pickle python module.

Usage:

	from database import data

	database = data.get_data()	# Gets the data from the database
	print(database) # Prints { 'users': [{'user_id': 1, 'name': 'Raymond'}, {'user_id': 2, 'name': 'Zeu'}] }

	users = database['users']

	users.pop(0) 	# Removes the item in index 0 of the list, this case, the item with user_id 1
	users.append({'user_id': 3, 'name': 'Yuqiang'})

	data.save_data(database)	# Saves the data to the database
'''

data_object = {
	'users': [],
}

class Database:
	def __init__(self):
		self.__data = data_object

	def get_data(self):
		return self.__data

	def save_data(self, new):
		if not isinstance(new, dict):
			raise TypeError("not type dictionary")
		self.__data = new

print("Loading Database...")

global data
data = Database()