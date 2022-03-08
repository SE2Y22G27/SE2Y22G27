import pytest
from source.register import register
from source.test_clear import clear

@pytest.fixture
def initial_clear():
	clear()

@pytest.fixture
def register_a():
	register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
	return register_info

@pytest.fixture
def register_b():
	register_info = register("testB@gmail.com", "1234567890", "Person", "BB")
	return register_info

@pytest.fixture
def register_c():
	register_info = register("testC@gmail.com", "1234567890", "Person", "CC")
	return register_info

def test_invalid_email(initial_clear):
	with pytest.raises(Exception):
		register("hellothere", "password", "Person", "Person")

def test_email_exists(initial_clear, register_a):
	with pytest.raises(Exception):
		register("testA@gmail.com", "1234567890", "Person", "AA")

def test_invalid_password_length(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com","A", "Person", "Person")

def test_invalid_name_length1(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "", "Person")

def test_invalid_name_length2(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "Person", "")

def test_invalid_name_length3(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "nameismorethanthirtytocheckthatthisworks", "Person")

def test_invalid_name_length4(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "Person", "nameismorethanthirtytocheckthatthisworks")

def test_invalid_name_length5(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "", "")

def test_invalid_name_length6(initial_clear):
	with pytest.raises(Exception):
		register("test@gmail.com", "password", "nameismorethanthirtytocheckthatthisworks", "nameismorethanthirtytocheckthatthisworks")

def test_name_edge_case(initial_clear):
	id0 = register("test0@gmail.com", "password", "I", "Person")
	id1 = register("test1@gmail.com", "password", "Person", "I")
	id2 = register("test2@gmail.com", "password", "I", "I")
	id3 = register("test3@gmail.com", "password", "nameisexactlythirtytocheck1234", "Person")
	id4 = register("test4@gmail.com", "password", "Person", "nameisexactlythirtytocheck1234")
	id5 = register("test5@gmail.com", "password", "nameisexactlythirtytocheck1234", "nameisexactlythirtytocheck1234")
	id6 = register("test6@gmail.com", "password", "I", "nameisexactlythirtytocheck1234")
	id7 = register("test7@gmail.com", "password", "nameisexactlythirtytocheck1234", "I")
	num = [0,1,2,3,4,5,6,7]
	ids = [id0,id1,id2,id3,id4,id5,id6,id7]
	
	for i in range(8):
		assert num[i] == ids[i]['auth_user_id']

def test_register_success(initial_clear, register_a):
	assert register_a['auth_user_id'] == 0

def test_multiple_registers(initial_clear, register_a, register_b, register_c):
	assert register_a['auth_user_id'] != register_b['auth_user_id'] != register_c['auth_user_id']
	assert register_a['token'] != register_b['token'] != register_c['token']