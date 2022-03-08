from source.database import data

def clear():
	'''
	Clear function to reset the internal data of the database

	IMPORTANT!
	This function should only be used in testing.
	It would be a massive data vulnerability if this was
	accessed during regular operation of our service.
	'''
	database = data.get_data()
	database['users'] = []
	data.save_data(database)