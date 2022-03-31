'''
	import all module to test of the register function is working normally
'''
import pytest
from source.register import register
from source.test_clear import clear
from source.error import InputError

def test_invalid_email():
    '''
		test invalid email format
	'''
    clear()
    with pytest.raises(InputError):
        register("hellothere", "password", "Person", "Person")

def test_email_exists():
    '''
		test an email has already exist in the system
	'''
    clear()
    register("testA@gmail.com", "1234567890", "Person", "AA")
    with pytest.raises(InputError):
        register("testA@gmail.com", "1234567890", "Person", "AA")

def test_invalid_password_length():
    '''
		test register an account with invalid password length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com","A", "Person", "Person")

def test_invalid_name_length1():
    '''
		test when register an account with invalid
		first name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password", "", "Person")

def test_invalid_name_length2():
    '''
		test when register an account with invalid
		last name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password", "Person", "")

def test_invalid_name_length3():
    '''
		test when register an account with invalid
		first name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password",
                    "nameismorethanthirtytocheckthatthisworks", "Person")

def test_invalid_name_length4():
    '''
		test when register an account with invalid
		last name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password", "Person",
					"nameismorethanthirtytocheckthatthisworks")

def test_invalid_name_length5():
    '''
		test when register an account with invalid
		first and last name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password", "", "")

def test_invalid_name_length6():
    '''
		test when register an account with invalid
		first and last name length
	'''
    clear()
    with pytest.raises(InputError):
        register("test@gmail.com", "password",
					"nameismorethanthirtytocheckthatthisworks",
					"nameismorethanthirtytocheckthatthisworks")

def test_name_edge_case():
    '''
		test when register an account with different edge cases
	'''
    clear()
    id0 = register("test0@gmail.com", "password", "I", "Person")
    id1 = register("test1@gmail.com", "password", "Person", "I")
    id2 = register("test2@gmail.com", "password", "I", "I")
    id3 = register("test3@gmail.com", "password",
					"nameisexactlythirtytocheck1234", "Person")
    id4 = register("test4@gmail.com", "password", "Person",
					"nameisexactlythirtytocheck1234")
    id5 = register("test5@gmail.com", "password",
					"nameisexactlythirtytocheck1234",
							"nameisexactlythirtytocheck1234")
    id6 = register("test6@gmail.com", "password",
					"I", "nameisexactlythirtytocheck1234")
    id7 = register("test7@gmail.com", "password",
					"nameisexactlythirtytocheck1234", "I")

    num = [0,1,2,3,4,5,6,7]
    ids = [id0,id1,id2,id3,id4,id5,id6,id7]

    for i in range(8):
        assert num[i] == ids[i]['auth_user_id']

def test_register_success():
    '''
		test register successfully
	'''
    clear()
    register_a = register("testA@gmail.com", "1234567890", "Person", "AA")
    assert register_a['auth_user_id'] == 0

def test_multiple_registers():
    '''
		test register multiple user successfully
	'''
    clear()
    register_a = register("testA@gmail.com", "1234567890", "Person", "AA")
    register_b = register("testB@gmail.com", "1234567890", "Person", "BB")
    register_c = register("testC@gmail.com", "1234567890", "Person", "CC")
    assert register_a['auth_user_id'] != register_b['auth_user_id'] != register_c['auth_user_id']
    assert register_a['token'] != register_b['token'] != register_c['token']
    
